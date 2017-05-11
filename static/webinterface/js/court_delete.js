$('#court_delete').click(function(event) {
    event.preventDefault();
    if(confirm('Sahayı silmek istediğinize emin misiniz?')) {
        $('#delete_form').submit();
    }
});
