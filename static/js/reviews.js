$(document).ready(function() {
   $('.btn-choose-firm').click(function() {
         var firm_id=$(this).attr('data-id');
         $.ajax({
                url: 'getTags/',
                data: { 'firm_id': firm_id},
                datatype: 'json',
                success: function (result) {
                   alert(result);
                },
               error: function(error) {
                   console.log(error.message);
                   return error;
               }
            });
   });
});