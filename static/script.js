function SearchFunction() {
  // let searchbtn = document.getElementById("searchbtn");
  let searchvalue = document.getElementById("searchval").value;

  $.post( "/search", {
    data: searchvalue
  });
};

// $.get("/retrievegithubdata", function(data) {
//     console.log($.parseJSON(data))
// })