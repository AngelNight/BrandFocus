      function addTag(){
        var keyWords = document.getElementById('keyWords').value;
        $.ajax({
                url: 'http://http://52.173.87.160//insertTag/',
                data: { 'name': keyWords,
                        'firm_id': $('.selectedButton').attr("data-id")
                        },
                datatype: 'json',
                success: function (result) {
                   var dataTagId = result;
                   if ($('.tagCompany[data-tag_id="' + dataTagId + '"]').length === 0){
                     document.getElementById('keyWords').value = "";
                     var newTag = document.createElement('div');
                     newTag.className = "tagCompany";
                     newTag.setAttribute('data-tag_id', dataTagId);
                     newTag.innerHTML =  keyWords + " &times;";
                     document.getElementById('workingArea').appendChild(newTag);
                     newTag.addEventListener("click", deleteMySelf);
                   }
                   this.disabled = true;
                },
               error: function(error) {
                   console.log(error.message);
                   return error;
               }
            });

      }
      function deleteMySelf(){
        var tagElement = $(this),
            tagId = $(this).attr('data-tag_id');
          $.ajax({
                url: 'http://http://52.173.87.160//deleteTag/?tag_id=' + tagId,
                data: { },
                datatype: 'json',
                success: function (result) {
                   tagElement.remove();
                },
               error: function(error) {
                   console.log(error.message);
                   return error;
            }
          });
      }
    });
}
function checkingBox(){
  var inputTag = document.getElementById('keyWords').value;
  var regExp
  if (inputTag.length > 1 /*&& inputTag.search(+)!=-1*/){
    $("#addBtn").removeAttr("disabled");
  }
}

function placeTags(result){
    var tagSpace = document.getElementById("workingArea");
    while(tagSpace.firstChild){
      tagSpace.removeChild(tagSpace.firstChild);
    }
    var tagsArr = JSON.parse(result);
    for (var i=0; i<tagsArr.length; i++)
    {
        var curTag = document.createElement ('div');
        curTag.className = "tagCompany";
        curTag.innerHTML = keyWords + " &times;";
        document.getElementById("workingArea").appendChild(curTag);
        curTag.addEventListener("click", deleteMySelf);
    }
}

function rankCode(btn_id){
  switch(btn_id){
    case 'pos':
      return 1;
    case 'neg':
      return -1;
    case 'any':
      return 0;
    case 'all':
      return 2;
  }
}

function setReviewColor(rank){
  switch(rank){
    case -1:
      return '#ffefed';
    case 0:
      return '#f8f8f8';
    case 1:
      return '#e8ffeb';
    case -100||-200:
      return -1;
  }
}

function postToHTML(){}

function placeReviews(result, btn_id){
  var reviewsArr = JSON.parse(result);
  var str = "";
  var color;

  var feedbacks = document.getElementById("lenta");
  while(feedbacks.firstChild){
    feedbacks.removeChild(feedbacks.firstChild);
  }

  for(var i = 0; i<reviewsArr.length, rankCode(btn_id)>=-1&&rankCode(btn_id)<=2; i++){
    if(rankCode(btn_id)>=-1&&rankCode(btn_id)<=1){
      color = setReviewColor(reviewsArr[i].rank)

      str += '<div class = "fb_head row"><div class = "col-sm-6 social_nw row">';
      str += '<img src = "'+reviewsArr[i].photolink+'" id = "avatar">';
      str += '<p id = "username">'+reviewsArr[i].name+'</p>';
      str += '<button type="button" class="btn btn-lg btn-link"><p id = "social_nw_name">'+reviewsArr[i].social_id+'</p></button>';
      str += '<p id = "feedback_date">'+reviewsArr[i].date+'</p></div>';
      str += '<div class = "col-sm-6 mistake_btn">';
      str += '<button type="button" class="btn btn-link dropdown-toggle" data-toggle="dropdown"><span class="caret" float="right">Ошибка</span></button>';
      str += '<ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu3"><li role="presentation"><a role="menuitem" href="#">Положительный</a></li>';
      str += '<li role="presentation"><a role="menuitem" href="#">Отрицательный</a></li><li role="presentation"><a role="menuitem" href="#">Неопределенный</a></li></ul></div>';
      str += '</div><div class = "feedback_text"><p id = "fb_text">'+ reviewsArr[i].text +'</p>';
      if(reviewsArr[i].img!="")
        str += '<img src = "'+ reviewsArr[i].img + '">';
      str += '</div>';

      var curPost = document.createElement ('div');
      curPost.className("feedback");
      curPost.style.background-color = color;
      curPost.innerHTML(str);
    }
  }
}

$(document).ready(function() {
  $('#upd').click(function() {
    var firm_id = $('.btnChooseFirm').hasClass('selectedButton').attr('data-id');
    $.ajax({
      url: 'http://http://52.173.87.160//getReviewsData/?firm_id='+firm_id,
      data: { 'firm_id': firm_id},
      datatype: 'json',
      success: function (result) {
         placeReviews(result, 2);
      },
     error: function() {
         alert("Error");
         return;
     }
    });
  });
})

$(document).ready(function() {
  $('.btn btn-default').click(function() {
    var btn_id = $(this.attr('id'));
    var firm_id = $('.btnChooseFirm').hasClass('selectedButton');
    $.ajax({
      url: 'http://http://52.173.87.160//getReviewsData/?firm_id='+firm_id,
      data: { 'firm_id': firm_id, 'btn_id': btn_id},
      datatype: 'json',
      success: function (result, btn_id ) {
         placeReviews(result, btn_id);
      },
     error: function() {
         alert("Error");
         return;
     }
    });
  });
})

$(document).ready(function() {
   $('.btnChooseFirm').click(function() {
   $('.selectedButton').removeClass('selectedButton');
   $(this).addClass('selectedButton');
   var firm_id=$(this).attr('data-id');
   $.ajax({
      url: '',
      data: { 'firm_id': firm_id},
      datatype: 'json',
      success: function (result) {
         placeTags(result);
      },
     error: function() {
         alert("Error");
         return;
     }
   });
});
})

addBtn.addEventListener("click", addTag);
$("#keyWords").keypress(checkingBox);
