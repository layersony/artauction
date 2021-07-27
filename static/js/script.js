$(document).ready(function(){
  $("#id_startTime").datetimepicker({
    format: 'Y-m-d H:i:i',
    formatTime: 'H:i:i',
    formatDate: 'Y-m-d',
  });
  $("#id_EndTime").datetimepicker(
    {
      format: 'Y-m-d H:i:i',
      formatTime: 'H:i:i',
      formatDate: 'Y-m-d',
    }
  );

  
});