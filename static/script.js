function SearchFunction() {
  // let searchbtn = document.getElementById("searchbtn");
  let searchvalue = document.getElementById("searchval").value;

  $.post( "/searchvalue", {
    data: searchvalue
  });
};

// $.get("/retrievegithubdata", function(data) {
//     console.log($.parseJSON(data))
// })

document.getElementById('search-text').hover = function() {
	document.getElementById('search-text').classList.toggle('show');
}