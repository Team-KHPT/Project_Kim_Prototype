// When the page is loaded, focus on the chat input field
$(document).ready(function() {
    $('#chat-input').focus();
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
        var userContainer = $('<div class="chat-container"></div>');
        userContainer.append($('<p></p>').text(message));
        $('#chat-messages').append(userContainer);

        // Create a message object with the user's message
        var messageObject = {
            role: 'user',
            content: message
        };

        // Send a POST request to the server with all the chat messages as JSON
        var chatMessages = $('#chat-messages').children().map(function() {
            var role = $(this).hasClass('received') ? 'assistant' : 'user';
            var content = $(this).find('p').text();
            return {
                role: role,
                content: content
            };
        }).get();

        $('#chat-input').val('');

        $.ajax({
            type: 'POST',
            url: '/chat',
            data: JSON.stringify(chatMessages),
            contentType: 'application/json',
            success: function(data) {
                // If the server successfully receives the chat messages, clear the input field
                if (data.status === 'success') {
                    // If the server returns a message, add it to the chat messages container
                    if (data.message) {
                        var assistanceContainer = $('<div class="chat-container received"></div>');
                        assistanceContainer.append($('<p></p>').text(data.message.content));
                        $('#chat-messages').append(assistanceContainer);

                        // Scroll the chat messages container to the bottom
                        $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);
                    }
                }
            }
        });

        // Scroll the chat messages container to the bottom
        $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);
    }
});
