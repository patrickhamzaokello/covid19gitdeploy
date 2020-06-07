function mytableFunction() {

var input, filter, tbody, tr, td, i;

input = document.getElementById("tablesearch");
filter = input.value.toUpperCase();

tbody = document.getElementById("tablebody");

tr = tbody.getElementsByTagName("tr");


for (i = 0; i < tr.length; i++) {

td = tr[i].getElementsByTagName("td")[0];

if ({{search}}.toUpperCase().indexOf(filter) > -1) {
tr[i].style.display = "";
} else {
tr[i].style.display = "none";
}

}

}
