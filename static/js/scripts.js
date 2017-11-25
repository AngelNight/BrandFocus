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
     function checkingBox(){
        var inputTag = document.getElementById('keyWords').value;
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
          var tagItem;
          for (var i=0, len=tagsArr.length; i<len; i++)
          {
              var curTag = document.createElement ('div');
              curTag.className = "tagCompany";
              tagItem = tagsArr[i];
              curTag.innerHTML = tagItem.fields.name + " &times;";
              $(curTag).attr('data-tag_id', tagItem.pk);
              document.getElementById("workingArea").appendChild(curTag);
              curTag.addEventListener("click", deleteMySelf); 
          }
      }
      $(document).ready(function() {
         $('.btnChooseFirm').click(function(event) {
            $('.selectedButton').removeClass('selectedButton');
            var elem = $(event.target).closest('.btnChooseFirm');
            elem.addClass('selectedButton');
            var firm_id = elem.attr('data-id');
            $.ajax({
                url: '/getTags/?firm_id=' + firm_id,
                data: { },
                datatype: 'json',
                success: function (result) {
                   console.log(result);
                   if ( result !== 'False' ){
                       placeTags(result);
                   }
                },
               error: function(error) {
                   console.log(error.message);
                   return error;
               }
            });
        });
     });

      addBtn.addEventListener("click", addTag);
      $("#keyWords").keypress(checkingBox);

