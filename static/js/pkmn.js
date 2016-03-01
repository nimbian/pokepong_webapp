var pkmn_list = []
function checkboxlimit(checkgroup, limit){
	var checkgroup=checkgroup
	var limit=limit
	for (var i=0; i<checkgroup.length; i++){
		checkgroup[i].onclick=function(){
		if(this.checked){
			pkmn_list.push(this.id);
		}
		var checkedcount=0
		if (pkmn_list.length>limit){
			alert("You can only select a maximum of "+limit+" Pokemon")
			this.checked=false
			}
		if (!this.checked){
			var index = pkmn_list.indexOf(this.id);
			if (index > -1){
				pkmn_list.splice(index, 1);
			}
		}
		console.log(pkmn_list)
		}
	}
}

function submit(){
	var team = document.getElementById("usr").value;
	if (!checkteam(team)){
		return
	}
	if (pkmn_list.length != 6){
		alert("Must choose 6 pkmn")
		return
	}
	success(team, pkmn_list)
}

function randomize(){
	var team = document.getElementById("usr").value;
	if (!checkteam(team)){
		return
	}
	pkmns = []
	while (pkmns.length < 6){
		var rand = Math.floor((Math.random() * 150) + 1);
		if (pkmns.indexOf(rand) < 0){
			pkmns.push(rand)
		}
	}
	success(team, pkmns)
}

function success(team, pkmn){
	$.ajax({
		url: '/checkUser',
		data: {'team':team},
		type: 'GET',
		success: function(res) {
			console.log(res);
			if (res['res']){
				window.location.replace("http://pokepong/"+team+"/"+pkmn)
			}
			else{
				alert('Team name already in use')
				return
			}
		},
		error: function(err){
			console.log('err')
		}
	})
}

function checkteam(team){
	if (team === ''){
		alert("Must enter a team name!")
		return false
	}
	if ( /[^a-zA-Z0-9]/.test( team )) {
		alert("Team name must only contain characters and numbers")
		return false
	}
	return true
}
	
