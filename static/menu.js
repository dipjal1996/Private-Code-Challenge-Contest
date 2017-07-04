function sure(id){
    
   if (confirm("Hey! Are you sure you want to accept request for contest: " + id) == true)
    {
        document.getElementById("data_id").value = id;
        document.go.submit();
    }

}

function start(id){
    
   if (confirm("Hey! Are you sure you want to start the contest: " + id) == true)
    {
        document.getElementById("data_id2").value = id;
        document.go1.submit();
    }

}