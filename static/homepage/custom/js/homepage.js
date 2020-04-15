function submitRequests(employees, reviewee_id) {
    console.log(employees);
    $.post("submitRequests", {
            csrfmiddlewaretoken: "{{ csrf_token }}",
            employees: employees,
            reviewee_id: reviewee_id
        },
        function(data, status) {
            const feedback_element = document.getElementById("new_requests_feedback");
            feedback_element.innerHTML = '<font size="2.7">' + data + '</font>';
            feedback_element.hidden = false;
        }
    );
}

function submitRequest(reviewee_email) {
    const reviewer_email = document.getElementById("coworker_email_input").value;
    $.post("request_review_post", {
            csrfmiddlewaretoken: "{{ csrf_token }}",
            reviewee_email: reviewee_email,
            reviewer_email: reviewer_email
        },
        function(data, status) {
            const feedback_element = document.getElementById("new_request_feedback");
            const draft_textarea = document.getElementById("")
                // feedback_element.innerHTML = data;
            feedback_element.innerHTML = '<font size="2.7">' + data + '</font>';
            feedback_element.hidden = false;
        }
    );
}

function submitDraft(review_id, status) {
    console.log("submitDraft");
    const draft_text = document.getElementById("draft_text").value;
    $.post("submit_draft_post", {
            csrfmiddlewaretoken: "{{ csrf_token }}",
            review_id: review_id,
            status: status,
            draft_text: draft_text
        },
        function(data, stat) {
            if (status === "S") {
                document.getElementById("draft" + review_id).hidden = true;
            }

            const draft_feedback = document.getElementById("draft" + review_id + "_feedback");
            draft_feedback.innerHTML = data
            draft_feedback.hidden = false;
        }
    );
}

function navClick(isReviews) {
    // Called when the 'Reviews' and 'Requests' buttons are pressed
    // Toggles which view is being shown
    if (isReviews) {
        document.getElementById("reviews").hidden = false;
        document.getElementById("requests").hidden = true;
        document.getElementById("review_button").disabled = true;
        document.getElementById("request_button").disabled = false;
    } else {
        document.getElementById("reviews").hidden = true;
        document.getElementById("requests").hidden = false;
        document.getElementById("review_button").disabled = false;
        document.getElementById("request_button").disabled = true;
    }
}

function requestClick(request_id, status) {
    $.post("accept_deny_request", {
            csrfmiddlewaretoken: "{{ csrf_token }}",
            request_id: request_id,
            status: status,
        },
        function(data, stat) {
            data = JSON.parse(data);
            feedback = data["feedback"]
            var accept_id = request_id + "-accept"
            var deny_id = request_id + "-deny"
            document.getElementById(accept_id).hidden = true;
            document.getElementById(deny_id).hidden = true;

            const request_feedback = document.getElementById("request" + request_id + "_feedback");
            if (status === "A") {
                draft_id = data["id"]
                draft_reviewee = data["reviewee"]

                request_feedback.innerHTML =
                    data["feedback"] + '\
    <div class="subcontent" id="draft' + draft_id + '"">\
      <div class="draft_head">\
        Your draft to ' + draft_reviewee + ':\
      </div>\
      <textarea id="draft_text" placeholder="write review..."></textarea>\
      <br>\
      <button onClick="submitDraft(' + draft_id + ', \'E\');">Save Draft</button>\
      <button onClick="submitDraft(' + draft_id + ', \'S\');">Send Review</button>\
    </div>\
    <div class="subcontent" id="draft' + draft_id + '_feedback" hidden></div>';

            } else if (status === "D") {
                request_feedback.innerHTML = data["feedback"]
            }

            request_feedback.hidden = false;
        }
    );
}