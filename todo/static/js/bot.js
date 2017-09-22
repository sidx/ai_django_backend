const bot = new ApiAi.ApiAiClient({accessToken: 'bdc1904d09de4420964286b9386fb254'});


function handleResponse(serverResponse) {
    console.log(serverResponse);
}

function handleError(serverError) {
    console.log(serverError);
}

/** chat **/
var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(document).ready(function () {
    $messages.mCustomScrollbar();
    setTimeout(function () {
        if ('speechSynthesis' in window) {
            var i = 1;
            window.speechSynthesis.onvoiceschanged = function () {
                if(i === 1)
                    botResponse('');
                i++;
            }
        } else {
            botResponse('');
        }
    }, 100);
});


function updateScrollbar() {
    $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
        scrollInertia: 10,
        timeout: 0
    });
}

function setDate() {
    d = new Date();
    if (m !== d.getMinutes()) {
        m = d.getMinutes();
        $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
        $('<div class="checkmark-sent-delivered">&check;</div>').appendTo($('.message:last'));
        $('<div class="checkmark-read">&check;</div>').appendTo($('.message:last'));
    }
}

function insertMessage() {
    msg = $('.message-input').val();
    if ($.trim(msg) === '') {
        return false;
    }

    $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    $('.message-input').val(null);
    updateScrollbar();
    const promise = bot.textRequest(msg);

    promise
        .then(function (response) {
            console.log(response);
            var response_message = '';
            setTimeout(function () {
                if (response['result']['action'].match(/smalltalk/g)) {
                    response_message = response['result']['fulfillment']['messages'][0]['speech'];
                } else {
                    response_message = response['result']['fulfillment']['speech'];
                }
                botResponse(response_message);
            }, 1000 + (Math.random() * 20) * 100);
        })
        .catch(handleError);
}

$('.message-submit').click(function () {
    insertMessage();
});

$(window).on('keydown', function (e) {
    if (e.which === 13) {
        insertMessage();
        return false;
    }
});

var Fake = [
    'Hi there, I\'m Jinx and how are you?',
];

function botResponse(message) {
    if ($('.message-input').val() !== '' || typeof  $('.message-input').val() === 'undefined') {
        return false;
    }
    $('<div class="message loading new"><figure class="avatar"><img src="/static/img/bot.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
    updateScrollbar();

    setTimeout(function () {
        $('.message.loading').remove();
        if ($.trim(message) === '') {
            message = Fake[i]
        }
        if(typeof message === 'undefined'){
            return false;
        }
        $('<div class="message new"><figure class="avatar"><img src="/static/img/bot.png" /></figure>' + message + '</div>').appendTo($('.mCSB_container')).addClass('new');
        if ('speechSynthesis' in window) {
            var msg = new SpeechSynthesisUtterance();
            var voices = window.speechSynthesis.getVoices();
            msg.voice = voices[3];
            msg.rate = 1;
            msg.pitch = 1;
            msg.text = message;
            speechSynthesis.speak(msg);
        }

        setDate();
        updateScrollbar();
        i++;
    }, 1000 + (Math.random() * 20) * 100);

}

$('.button').click(function () {
    $('.menu .items span').toggleClass('active');
    $('.menu .button').toggleClass('active');
});