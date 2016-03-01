for (i = 1; i <= 150; i++){
	var newinput = document.createElement('input');
	var newlabel = document.createElement('label');
	newinput.type = 'checkbox';
	newinput.name = 'pkmn';
	newinput.value = i;
	newinput.id = i;
	newlabel.className = 'pkmn';
	newlabel.setAttribute("for", i);
	var newimg = document.createElement('i')
	newimg.className = "sprite sprite-" + i;
	newimg.style = 'margin-left: 35px; margin-top: 35px';
	newlabel.appendChild(newimg);
	document.getElementById("pkmns").appendChild(newinput);
	document.getElementById("pkmns").appendChild(newlabel);
}
checkboxlimit(document.forms.pkmns.pkmn,6)
