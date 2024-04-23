function editClicked(toDoId,toDoInput){
    document.querySelector('.ul')
        .style.filter = "blur(5px)";
        
    document.querySelector('.edit-div')
        .innerHTML = `
        <form action="edit-toDo" method="post">
                    <input type="text" value = "${toDoInput}" name="toDoInput">                      

                    <input type="hidden" value="${toDoId}" name="toDoId">
                    <input type="submit" value="Save">
        </form>
        `
}