      function addTag(){
        var keyWords = document.getElementById('keyWords').value;
        /*var inputData{
          "tagName":$("#keyWords").val()
        };
       $.ajax({
                    url:'dataparser.php'
                    , type:'POST'
                    , data:'jsonData=' + $.toJSON(formData)
                    , success: function(res) {
                        alert(res);
                    }
                });*/
        document.getElementById('keyWords').value = "";
        var newTag = document.createElement('div');
        newTag.className = "tagCompany";
        newTag.innerHTML =  keyWords + " &times;";
        document.getElementById('workingArea').appendChild(newTag);
        newTag.addEventListener("click", deleteMySelf);
        this.disabled = true;
      }
      function deleteMySelf(){
          this.remove();
      }
     function checkingBox(){
        var inputTag = document.getElementById('keyWords').value;
        if (inputTag.length > 1 /*&& inputTag.search([A-Za-zА-Яа-я]+)!=-1*/){
          $("#addBtn").removeAttr("disabled");
        }
      }
      addBtn.addEventListener("click", addTag);
      $("#keyWords").keypress(checkingBox);