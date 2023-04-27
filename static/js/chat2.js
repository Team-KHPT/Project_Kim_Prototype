// When the page is loaded, focus on the chat input field
$(document).ready(function() {
    $('#chat-input').focus();
    $("#spinner").css("display", "block");
    $('#spinner').hide()
    opening()
});

// When the chat form is submitted
$('#chat-form').submit(function(e) {
    // Prevent the form from submitting normally
    e.preventDefault();

    // Get the message from the input field
    var message = $('#chat-input').val();

    // If the message is not empty
    if (message.trim() !== '') {
        // Add the user's message to the chat messages container
        var userContainer = $('<div class="chat"></div>');
        userContainer.append($('<div class="user_chat"></div>').append($('<p></p>').text(message)));
        $('#chat-messages').append(userContainer);


        // Send a POST request to the server with all the chat messages as JSON
        var chatMessages = $('#chat-messages').children().map(function() {
            var role = $(this).hasClass('received') ? 'assistant' : 'user';
            var content = $(this).children(':last-child').find('p').text();
            return {
                role: role,
                content: content
            };
        }).get();
        $('#chat-input').val('');

        console.log(chatMessages)

        function csrfSafeMethod(method) {
            // These HTTP methods do not require CSRF protection
            return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    const csrftoken = Cookies.get('csrftoken');
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });

        var isFirstChunk = true

        $.ajax({
            type: 'POST',
            url: '/chat',
            data: JSON.stringify(chatMessages),
            contentType: 'application/json',
            xhrFields: {
                    // Set up the XHR object to receive server responses as a stream
                    onprogress: function(e) {
                        if (e.currentTarget.readyState === 3) {

                            // When the server sends a message as a stream, parse it as JSON and add it to the chat messages container
                            console.log(e.currentTarget.responseText)
                            var message= e.currentTarget.responseText
                            var assistanceContainer = $('<div class="chat received"></div>');
                            if (isFirstChunk) {
                                assistanceContainer.append($('<div class="assistance_chat"></div>')
                                    .append($('<div class="assistance_profile"><img src="https://blog.kakaocdn.net/dn/b8Kdun/btqCqM43uim/1sWJVkjEEy4LJMfR3mcqxK/img.jpg"></div>'))
                                    .append($('<p></p>').text(message)));
                                $('#chat-messages').append(assistanceContainer);

                                // Scroll the chat messages container to the bottom
                                $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);

                                isFirstChunk = false
                            } else {

                                $('#chat-messages').children(':last-child').children(':last-child').children(':last-child').text(message)

                                console.log(message)
                            }
                            $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);

                        }
                    }
                },
            success: function(data) {
                console.log('success')
            }
        });

        // Scroll the chat messages container to the bottom
        $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);
    }
});

$('#chat-analyze').click(function(e) {
    // Prevent the form from submitting normally
    e.preventDefault();

    console.log("show")
    $('#spinner').show()

    // Send a POST request to the server with all the chat messages as JSON
    var chatMessages = $('#chat-messages').children().map(function() {
        var role = $(this).hasClass('received') ? 'assistant' : 'user';
        var content = $(this).find('p').text();
        return {
            role: role,
            content: content
        };
    }).get();

    function csrfSafeMethod(method) {
        // These HTTP methods do not require CSRF protection
        return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                const csrftoken = Cookies.get('csrftoken');
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });

    console.log(chatMessages)

    if (chatMessages.length > 2) {
        $.ajax({
            type: 'POST',
            url: '/chat/analyze',
            data: JSON.stringify(chatMessages),
            contentType: 'application/json',

            success: function(data) {
                console.log("hide suc")
                $('#spinner').hide()
                console.log(data)
                let jobList = data.jobs

                $('#analysis-list').empty()

                for(let job of jobList) {
                    let officeName = job.company.detail.name
                    let urlStr = job.url

                    $('#analysis-list').append($('<div class="analysis-data"></div>').append($(`<a target="_blank" href="${urlStr}"></a>`).append($('<span></span>').text(officeName))))

                    console.log(job)
                }
            }
        });

    } else {
        alert("먼저 채팅을 진행해 주세요")
    }

});

function opening() {
    function csrfSafeMethod(method) {
        // These HTTP methods do not require CSRF protection
        return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                const csrftoken = Cookies.get('csrftoken');
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });

    var isFirstChunk = true
    $.ajax({
        type: 'POST',
        url: '/chat/opening',
        contentType: 'application/json',
        xhrFields: {
                // Set up the XHR object to receive server responses as a stream
                onprogress: function(e) {
                    if (e.currentTarget.readyState === 3) {
                        // When the server sends a message as a stream, parse it as JSON and add it to the chat messages container
                        console.log(e.currentTarget.responseText)
                        var message= e.currentTarget.responseText
                        var assistanceContainer = $('<div class="chat received"></div>');
                        if (isFirstChunk) {
                            assistanceContainer.append($('<div class="assistance_chat"></div>')
                                .append($('<div class="assistance_profile"><img src="https://blog.kakaocdn.net/dn/b8Kdun/btqCqM43uim/1sWJVkjEEy4LJMfR3mcqxK/img.jpg"></div>'))
                                .append($('<p></p>').text(message)));
                            $('#chat-messages').append(assistanceContainer);

                            // Scroll the chat messages container to the bottom
                            $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);

                            isFirstChunk = false
                        } else {

                            $('#chat-messages').children(':last-child').children(':last-child').children(':last-child').text(message)

                            console.log(message)
                        }
                        $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);

                    }
                }
            },
        success: function(data) {
            console.log('success')
        }
    });
}
