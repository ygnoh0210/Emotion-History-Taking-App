const question  = function(){
  const question=$('#question-text').val();
  if(question.length > 0){
    $('.chat-list').append(`
      <li class="me">
        <span class="material-icons">face</span>
        ${question}
      </li>
    `)
    $('#question-text').val('')
  }
  $(".chat-thread").animate({ scrollTop: $('.chat-list').height() }, 1000);
}

$('#btn-question').on({
  click:question,
  keyup:function(key) {
    if(key.keyCode==13) {
      question()
    }
  }
});

$('#question-text').on({
  keyup:function(key) {
    if(key.keyCode==13) {
      question()
    }
  }
});