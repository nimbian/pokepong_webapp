var pkmn_list = [];
function checkboxlimit(checkgroup, limit){
	var checkgroup=checkgroup;
	var limit=limit;
	for (var i=0; i<checkgroup.length; i++){
		checkgroup[i].onclick=function(){
		if(this.checked){
			pkmn_list.push(this.id);
		}
		var checkedcount=0;
		if (pkmn_list.length>limit){
			alert("You can only select a maximum of "+limit+" Pokemon");
			this.checked=false;
			}
		if (!this.checked){
			var index = pkmn_list.indexOf(this.id);
			if (index > -1){
				pkmn_list.splice(index, 1);
			}
		}
		console.log(pkmn_list);
		}
	}
}

