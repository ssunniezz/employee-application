function openTab(evt, tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].style.backgroundColor = "";
  }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.style.backgroundColor = "#ddd";
}

// Open the default tab
document.getElementsByClassName("tablink")[0].click();

 document.addEventListener('DOMContentLoaded', function() {
        const filterBtn = document.getElementById('filterButton');
        const searchForm = document.getElementById('searchForm');
        filterBtn.addEventListener('click', function() {
            if (searchForm.style.display === 'none') {
                searchForm.style.display = 'block';
            } else {
                searchForm.style.display = 'none';
            }
        });
    });