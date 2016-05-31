function test(id){
    var cb = $('#pokemon-' + String(id - 1));
    cb.prop("checked", !cb.prop("checked"));
}
