      function addTag(){
        var keyWords = document.getElementById('keyWords').value;
        $.ajax({
                url: 'http://52.173.83.176/insertTag/',
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
                url: 'http://52.173.83.176/deleteTag/?tag_id=' + tagId,
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
/*
function filterReviews(id){
  switch(id){
    case 'all':
      placeReviews();
    case 'pos':
    case 'neg':
    case 'any':
  }
}
*/

function placeReviews(result, mode = 0){
  if(mode == 0)
    var reviewsArr = JSON.parse(result);
  var str = "";
  /*
  reviewsArr[1] - link
  2 - text
  3 - {-1(neg), 0(pos), 1(any), -100(spam), -200(ad)}
  4 - date
  6 - photolink
  7 - social_id
  8 - firm_id
  10 - name
  */

  var feedbacks = document.getElementById("lenta");
  while(feedbacks.firstChild){
    feedbacks.removeChild(feedbacks.firstChild);
  }

  for(var i = 0; i<reviewsArr.length; i++){
    var color;
    if(color = setReviewColor(reviewsArr[i].rank)==-1)
      break;

    str += '<div class = "fb_head row"><div class = "col-sm-6 social_nw row">';
    str += '<img src = "'+reviewsArr[i].photolink+'" id = "avatar">';
    str += '<p id = "username">'+reviewsArr[i].name+'</p>';
    str += '<button type="button" class="btn btn-lg btn-link"><p id = "social_nw_name">'+reviewsArr[i].social_id+'</p></button>';
    str += '<p id = "feedback_date">'+reviewsArr[i].date+'</p></div>';
    str += '<div class = "col-sm-6 mistake_btn">';
    str += '<button type="button" class="btn btn-link dropdown-toggle" data-toggle="dropdown"><span class="caret" float="right">Ошибка</span></button>';
    str += '<ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu3"><li role="presentation"><a role="menuitem" href="#">Положительный</a></li>';
    str += '<li role="presentation"><a role="menuitem" href="#">Отрицательный</a></li><li role="presentation"><a role="menuitem" href="#">Неопределенный</a></li></ul></div>';
    str += '</div><div class = "feedback_text"><p id = "fb_text">'+ reviewsArr[i].text +'</p></div>';

    var curPost = document.createElement ('div');
    curPost.className("feedback");
    curPost.style.background-color = color;
    curPost.innerHTML(str);
  }
}

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
   $.ajax({
      url: '',
      data: { 'firm_id': firm_id },
      datatype: 'json',
      success: function (result) {
         placeReviews(result);
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
