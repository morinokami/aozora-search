$(document).ready(function() {
  $('#category1').append($('<option>').html('大分類').val(''));
  $('#category2').append($('<option>').html('中分類').val(''));
  $('#category3').append($('<option>').html('小分類').val(''));


  $.ajax({
    url: 'http://' + location.host + '/data/1',
    dataType: 'json'
  }).done(function(data) {
    var keys = Object.keys(data);
    for (var i = 0, len = keys.length; i < len; i++) {
      var key = keys[i];
      var value = data[key];
      $('#category1').append($('<option>').val(key).html(value));
    }
  });


  $('#category1').change(function() {
    var selected = $('#category1').val();
    $.ajax({
      url: 'http://' + location.host + '/data/2',
      dataType: 'json'
    }).done(function(data) {
      var keys = [];
      var temp = Object.keys(data);
      for (var i = 0; i < temp.length; i++) {
        if (temp[i][0] == selected) {
          keys.push(temp[i]);
        }
      }
      $('#category2 option').each(function() { $(this).remove(); });
      $('#category2').append($('<option>').html('中分類').val(''));
      for (var j = 0, len = keys.length; j < len; j++) {
        var key = keys[j];
        var value = data[key];
        $('#category2').append($('<option>').val(key).html(value));
      }
    });

    $('#category3 option').each(function() { $(this).remove(); });
    $('#category3').append($('<option>').html('小分類').val(''));
  });


  $('#category2').change(function() {
    var selected = $('#category2').val();
    $.ajax({
      url: 'http://' + location.host + '/data/3',
      dataType: 'json'
    }).done(function(data) {
      var keys = [];
      var temp = Object.keys(data);
      for (var i = 0; i < temp.length; i++) {
        if (temp[i].slice(0, 2) == selected) {
          keys.push(temp[i]);
        }
      }
      $('#category3 option').each(function() { $(this).remove(); });
      $('#category3').append($('<option>').html('小分類').val(''));
      for (var j = 0, len = keys.length; j < len; j++) {
        var key = keys[j];
        var value = data[key];
        $('#category3').append($('<option>').val(key).html(value));
      }
    });
  });
});
