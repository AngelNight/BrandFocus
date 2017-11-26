var socialsdata;
$(document).ready(function() {
     $.ajax({
                url: 'getSocials/',
                data: {},
                datatype: 'json',
                success: function (result) {
                    if (result != false) {
                        socialsdata=$.parseJSON(result);
                        console.log(socialsdata);
                    }
                },
                error: function(error) {
                   console.log(error.message);
                   return error;
            }
          });
   $('.btnChooseFirm').click(function() {
       $('#keyWords').removeAttr('disabled');
       $('.btnChooseFirm').removeClass('btnChooseFirm-active');
       $(this).addClass('btnChooseFirm-active');
         var firm_id=$(this).attr('data-id');
         $.ajax({
                url: 'getTags/',
                data: { 'firm_id': firm_id},
                datatype: 'json',
                success: function (result) {
                    $('#workingArea').html("");
                    if (result != false) {
                        result=$.parseJSON(result);
                        $.each(result, function(index, element) {
                            $('#workingArea').append("<div class='tagCompany' >"+element['fields']['name']+"<span data-tag-id='"+element['pk']+"' class='deleteTag'>&times;</span></div>");
                       });
                       $('#workingArea').find('.tagCompany').find('.deleteTag').each(function() {
                           $(this).click(function() {
                              deleteTag($(this));
                           });
                       });
                    }
                },
               error: function(error) {
                   console.log(error.message);
                   return error;
               }
            });
       getLenta();
   });
   $('.btnChooseFirm').eq(0).trigger("click");
   $('#addBtn').click(function() {
       var name=$('#keyWords').val();
       var firmid=$('.btnChooseFirm-active').attr('data-id');
       $.ajax({
                url: 'insertTag/',
                data: { 'name': name, 'firm_id': firmid},
                datatype: 'json',
                success: function (result) {
                    $('.btnChooseFirm-active').trigger("click");
                    $('#keyWords').val("");
                },
                error: function(error) {
                   console.log(error.message);
                   return error;
                }
            });
   });
   $('.charmixFeedSort').click(function() {
      var rank=$(this).attr('data-sort');
      if (rank != "all") {
           $('.charmixFeed, .charmixFeedText').hide();
          $('.charmixFeed[data-rank-id="'+rank+'"]').show();
          $('.charmixFeedText[data-rank-id="'+rank+'"]').show();
      } else {
          $('.charmixFeed, .charmixFeedText').show();
      }
   });
   $('#feedUpdateBtn').click(function() {
       var firmid=$('.btnChooseFirm-active').attr('data-id');
       $('#feedUpdateBtn').text("Обновляется...");
       if (!$(this).hasClass('blocked')) {
           $.ajax({
                url: 'getReviews/',
                data: {'firm_id': firmid},
                datatype: 'json',
                success: function (result) {
                    $('#feedUpdateBtn').text("Обновить");
                    $('#feedUpdateBtn').removeClass('blocked');
                    $('.btnChooseFirm-active').trigger("click");
                },
                error: function(error) {
                   console.log(error.message);
                   return error;
                }
            });
       }

   });
});
function deleteTag(obj){
    var tagId=obj.attr('data-tag-id');
     $.ajax({
                url: 'deleteTag/?tag_id=' + tagId,
                data: { },
                datatype: 'json',
                success: function (result) {
                   obj.parent().remove();
                },
                error: function(error) {
                   console.log(error.message);
                   return error;
            }
          });
}
function getLenta() {
    var firmid=$('.btnChooseFirm-active').attr('data-id');
     $.ajax({
                url: 'getReviewsData/',
                data: { 'firm_id': firmid},
                datatype: 'json',
                success: function (result) {
                    $('.lenta_content').html("");
                    if (result != false) {
                        result=$.parseJSON(result);
                        $.each(result, function(index, element) {
                            str="";
                            soc_str="";
                            $.each(socialsdata, function(index2, element2) {
                                if(element2.pk == element.fields.social) {
                                    soc_str=element2.fields.name;
                                }
                            });
                            str="<div class='charmixFeed' data-rank-id='"+element['fields']['rank']+"'>";
                            str+="<img class='charmixFeed_logo' src='"+element['fields']['photo_link']+"'>";
                            str+="<p class='username'></p>";
                            str+="<a target='_blank' href='"+element['fields']['link']+"'>"+soc_str+"</a>";
                            str+="<p class='feedback_date'>"+element['fields']['date']+"</p>";
                            str+="</div>";
                            str+="<div class='charmixFeedText' data-rank-id='"+element['fields']['rank']+"'><p>"+element['fields']['text']+"</p></div>";
                            str+="</div>";
                            $('.lenta_content').append(str);
                       });
                       $('#workingArea').find('.tagCompany').find('.deleteTag').each(function() {
                           $(this).click(function() {
                              deleteTag($(this));
                           });
                       });
                       var countall=$('.charmixFeed').length;
                       $('#count_all').text(countall);
                       var countpos=$('.charmixFeed[data-rank-id=1]').length;
                       $('#count_pos').text(countpos);
                       var countany=$('.charmixFeed[data-rank-id=0]').length;
                       $('#count_any').text(countany);
                       $('#count_neg').text(countall-countpos-countany);
                    }
                },
               error: function(error) {
                   console.log(error.message);
                   return error;
               }
            });
}