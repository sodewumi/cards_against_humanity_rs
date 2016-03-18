$.ajax({
  url: '/player_list',
  type: 'GET',
})
  .done(function(data) {
    var engine = new Bloodhound({
      local: data.foo,
      datumTokenizer: function(d) {
        return Bloodhound.tokenizers.whitespace(d.value);
      },
      queryTokenizer: Bloodhound.tokenizers.whitespace
    });

    engine.initialize();

    $('#players').tokenfield({
      typeahead: [null, { source: engine.ttAdapter() }]
    });
  })
  .fail(function(data) {
    $('#players').tokenfield();
  })

$('#create-room').on('submit', function(evt) {

  if(($('#room_name').val() !== "") && $('div').hasClass('token') ) {
    usernamesList = []
    $('.token').map(function() {
      usernamesList.push($(this).find('span').text());
    });

    usernames = usernamesList.join(',')
    $('#players').val(usernames)

    return;
  }

  evt.preventDefault();
  console.log("error")

})
