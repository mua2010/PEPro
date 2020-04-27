function submitRequests(employees, reviewee_id) {
    console.log(employees);
    $.post("submit_requests", {
            csrfmiddlewaretoken: "{{ csrf_token }}",
            employees: employees,
            reviewee_id: reviewee_id
        },
        function(data, status) {
            data = JSON.parse(data);
            var feedback = data["feedback"];
            var private_status = data["private_status"];

            const feedback_element = document.getElementById("new_requests_feedback");

            feedback_element.className = "alert alert-success";

            if (private_status === 401) {
                feedback_element.className = "alert alert-danger";
            }
            if (private_status === 204) {
                feedback_element.className = "alert alert-info";
            }
            feedback_element.innerHTML = '<font size="2.7">' + feedback + '</font>';
            feedback_element.hidden = false;
        }
    );
}

// function submitRequest(reviewee_email) {
//     const reviewer_email = document.getElementById("coworker_email_input").value;
//     $.post("request_review_post", {
//             csrfmiddlewaretoken: "{{ csrf_token }}",
//             reviewee_email: reviewee_email,
//             reviewer_email: reviewer_email
//         },
//         function(data, status) {
//             const feedback_element = document.getElementById("new_request_feedback");
//             const draft_textarea = document.getElementById("")
//                 // feedback_element.innerHTML = data;
//             feedback_element.innerHTML = '<font size="2.7">' + data + '</font>';
//             feedback_element.hidden = false;
//         }
//     );
// }

function submitDraft(review_id, status) {
    console.log("submitDraft");
    var draft_text_id = "draft_text" + review_id
    var draft_text = document.getElementById(draft_text_id).value;
    $.post("submit_draft_post", {
            csrfmiddlewaretoken: "{{ csrf_token }}",
            review_id: review_id,
            status: status,
            draft_text: draft_text
        },
        function(data, stat) {
            if (status === "S") {
                document.getElementById("draft_text" + review_id).hidden = true;
                var save_id = review_id + "-save"
                var send_id = review_id + "-send"
                document.getElementById(save_id).hidden = true;
                document.getElementById(send_id).hidden = true;
                document.getElementById("draft_text" + review_id).hidden = true;
            }

            var draft_feedback = document.getElementById("draft" + review_id + "_feedback");
            draft_feedback.innerHTML = data
            draft_feedback.hidden = false;
        }
    );
}

// function navClick(isReviews) {
//     // Called when the 'Reviews' and 'Requests' buttons are pressed
//     // Toggles which view is being shown
//     if (isReviews) {
//         document.getElementById("reviews").hidden = false;
//         document.getElementById("requests").hidden = true;
//         document.getElementById("review_button").disabled = true;
//         document.getElementById("request_button").disabled = false;
//     } else {
//         document.getElementById("reviews").hidden = true;
//         document.getElementById("requests").hidden = false;
//         document.getElementById("review_button").disabled = false;
//         document.getElementById("request_button").disabled = true;
//     }
// }

function acceptDenyRequest(request_id, status) {
    $.post("accept_deny_request", {
            csrfmiddlewaretoken: "{{ csrf_token }}",
            request_id: request_id,
            status: status,
        },
        function(data, stat) {
            data = JSON.parse(data);
            var feedback = data["feedback"];
            var accept_id = request_id + "-accept";
            var deny_id = request_id + "-deny";
            document.getElementById(accept_id).hidden = true;
            document.getElementById(deny_id).hidden = true;

            var request_feedback = document.getElementById("request" + request_id + "_feedback");
            if (status === "A") {
                var draft_id = data["id"];
                console.log(draft_id);
                if (draft_id != null) {
                    var draft_reviewee = data["reviewee"];
                    request_feedback.innerHTML = data["feedback"];

                    var quick_draft = document.getElementById("quick_draft" + request_id);
                    quick_draft.innerHTML =
                        '<div class="form-check" id="draft' + draft_id + '">\
                            <div class="card border-dark mb-3" style="max-width: 50rem;">\
                                <div class="card-body text-dark">\
                                    <div class="form-group shadow-textarea">\
                                        <textarea class="form-control z-depth-1" id="draft_text' + draft_id + '" rows="3" placeholder="Write review here..."></textarea>\
                                    </div>\
                                    <button class="btn btn-secondary" id="' + draft_id + '-save" onClick="submitDraft(' + draft_id + ', \'E\');">Save Draft</button>\
                                    <button class="btn btn-success" id="' + draft_id + '-send" onClick="submitDraft(' + draft_id + ', \'S\');">Send Review</button>\
                                    <br><br>\
                                    <div class="alert alert-info" role="alert" id="draft' + draft_id + '_feedback" style="width: fit-content" hidden></div>\
                                </div>\
                            </div>\
                        </div>';

                    quick_draft.hidden = false;
                } else {
                    request_feedback.innerHTML = data["feedback"];
                    request_feedback.className = "alert alert-danger";
                }
            } else if (status === "D") {
                request_feedback.innerHTML = data["feedback"]
            }

            request_feedback.hidden = false;
        }
    );
}