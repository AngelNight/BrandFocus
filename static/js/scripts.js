function social(id){
  switch(id){
   case 1:
    return "Вконтакте";
   case 2:
    return "Twitter";
   case 3:
    return "Google";
   default:
    return "Unknown";
  }
}

function addTag(){
  var keyWords = document.getElementById('keyWords').value;
  $.ajax({
          url: 'http://52.173.87.160//insertTag/',
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
          url: 'http://52.173.87.160/deleteTag/?tag_id=' + tagId,
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

function checkingBox(){
  return $("#keyWords").val().length > 1? $("#addBtn").removeAttr("disabled") : $("#addBtn").attr("disabled", true);
}

function placeTags(result){
    var tagSpace = document.getElementById("workingArea"),
        keyWords;
    while(tagSpace.firstChild){
      tagSpace.removeChild(tagSpace.firstChild);
    }
    var tagsArr = JSON.parse(result);
    for (var i=0; i<tagsArr.length; i++)
    {
        var curTag = document.createElement ('div');
        keyWords = tagsArr[i].fields["name"];
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
  }
}

function createReview(reviewsArr, color){
  var str = "";
  str += '<div class = "fb_head row"><div class = "col-sm-6 social_nw row">';
  str += '<img src = "'+reviewsArr.fields.photo_link+'" id = "avatar">';
  str += '<p id = "username">Отзыв</p>';
  str += '<button type="button" class="btn btn-lg btn-link" onclick="window.location.href="'+reviewsArr.fields.link+'""><p id = "social_nw_name">'+social(reviewsArr.fields.social)+'</p></button>';
  str += '<p id = "feedback_date">'+reviewsArr.fields.date+'</p></div>';
  str += '<div class = "col-sm-6 mistake_btn">';
  str += '<button type="button" class="btn btn-link dropdown-toggle" data-toggle="dropdown"><span class="caret" float="right">Ошибка</span></button>';
  str += '<ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu3"><li role="presentation"><a role="menuitem" href="#">Положительный</a></li>';
  str += '<li role="presentation"><a role="menuitem" href="#">Отрицательный</a></li><li role="presentation"><a role="menuitem" href="#">Неопределенный</a></li></ul></div>';
  str += '</div><div class = "feedback_text"><p id = "fb_text">'+ reviewsArr[i].text +'</p>';
  str += '</div>';

  var curPost = document.createElement('div');
  curPost.className = "feedback";
  curPost.style["background-color"] = color;
  curPost.innerHTML = str;
  return curPost;
}

function placeReviews(result, btn_id){
  var reviewsArr = JSON.parse(result);
  var color;
  var feedbacks = document.getElementById("lenta");
  while(feedbacks.firstChild){
    $("#NoRev").hide();
    feedbacks.removeChild(feedbacks.firstChild);
  }
  var rankArr = [0, 0, 0, 0];
  for(var i = 0, ln = reviewsArr.length; i<ln, reviewsArr[i].fields.rank>=-1; i++){
      rankArr[reviewsArr[i].fields.rank + 1]++;
      color = setReviewColor(reviewsArr[i].fields.rank);
      
      if(btn_id==2)
        feedbacks.appendChild(createReview(reviewsArr[i], color));
      else if(btn_id==reviewsArr[i].fields.rank)
        feedbacks.appendChild(createReview(reviewsArr[i], color));
   }

   var all = reviewsArr.length;
   $('#count_all').html(all);
   $('#count_pos').html(rankArr[2]);
   $('#count_neg').html(rankArr[0]);
   $('#count_any').html(rankArr[1]);
}

function firmSelected() {
   $('.selectedButton').removeClass('selectedButton');
   $(this).addClass('selectedButton');
   var firm_id = $(this).attr('data-id');
   $.ajax({
      url: 'http://52.173.87.160/getTags/?firm_id=' + firm_id,
      data: {},
      datatype: 'json',
      success: function (result) {
         placeTags(result);
      },
     error: function(error) {
         alert("Error");
         return error;
     }
   });
}

function refreshReviews() {
    var firm_id = $('.btnChooseFirm.selectedButton').attr('data-id');
    if(!firm_id){
    $.ajax({
      url: 'http://52.173.87.160/getReviews/?firm_id=' + firm_id,
      data: {},
      datatype: 'json',
      success: function (result) {
         placeReviews(result, 2);
      },
     error: function() {
         alert("Error");
         return;
     }
    });
  }
}
function reviewsSelect(){
    var btn_id = $(this).attr('btn-id');
    var firm_id = $('.btnChooseFirm.selectedButton').attr('data-id');
    $.ajax({
      url: 'http://52.173.87.160/getReviewsData/?firm_id='+firm_id,
      data: {},
      datatype: 'json',
      success: function (result) {
         placeReviews(result, btn_id);
      },
     error: function(error) {
         console.log(error.message);
         return error;
     }
    });
  }

$(document).ready(function() {
  $('.btnChooseFirm').click(firmSelected);
  $('.counter').click(reviewsSelect);
  $("#addBtn").click(addTag);
  $("#keyWords").keypress(checkingBox);
  $('#upd').click(refreshReviews);
});
