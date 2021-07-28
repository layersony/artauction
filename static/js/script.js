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

  starttime = moment(document.getElementById('startingtimeind').textContent, 'MMMM DD YYYY H:mmA').toString()
  endtime = moment(document.getElementById('endingtimeind').textContent, 'MMMM DD YYYY H:mmA').toString()
  timestatus = $('#timestatusind')
  timewriting = $('#timewritingind')


 
  const starting = Date.parse(starttime)
  const ending = Date.parse(endtime)

  const mycountdown = setInterval(()=>{
    const now = new Date().getTime()

    const diff = starting - now 
    const toend = ending - now

    const d = Math.floor(starting/ (1000 * 60 * 60 * 24) - (now/ (1000 * 60 * 60 *24)))
    const h = Math.floor((starting/ (1000 * 60 * 60) - (now/ (1000 * 60 * 60))) % 24)
    const m = Math.floor((starting/ (1000 * 60) - (now/ (1000 * 60))) % 60)
    const s = Math.floor((starting/ (1000) - (now/ (1000))) % 60)

    const dtoend = Math.floor(ending/ (1000 * 60 * 60 * 24) - (now/ (1000 * 60 * 60 *24)))
    const htoend = Math.floor((ending/ (1000 * 60 * 60) - (now/ (1000 * 60 * 60))) % 24)
    const mtoend = Math.floor((ending/ (1000 * 60) - (now/ (1000 * 60))) % 60)
    const stoend = Math.floor((ending/ (1000) - (now/ (1000))) % 60)

    if(diff>0){
      if (d > 0){
        let todis = d + ' days ' + h + ' hours ' + m + ' mins ' + s + ' secs'
        timewriting.text('Starts In: ')
        timestatus.text(todis)
      }else if ( d> 0 || h > 0){
        let todis =  h + ' hours ' + m + ' mins ' + s + ' secs'
        timewriting.text('Starts In: ')
        timestatus.text(todis)
      }else{
        let todis =  m + ' mins ' + s + ' secs'
        timewriting.text('Starts In: ')
        timestatus.text(todis)
      }
    }else if (toend>0){
      let toendwhen = dtoend + ' days ' + htoend + ' hours ' + mtoend + ' mins ' + stoend + ' secs'
      timewriting.text('Ends In: ')
      timestatus.text(toendwhen)
        $.ajax({
          'url':'',
          'type':'',
          'data': {
            'artid':'{{ art.id}}',
            'csrfmiddlewaretoken':'{{ csrf_token }}',
          },
          'dataType':'json',
          'success': function(data){
            console.log(data)
          }
        })

    }else{
      clearInterval(mycountdown)
      timewriting.text('Ended: ')
      timestatus.text('--')
    }
  }, 1000)  
});