function(doc) { 
    if (doc.doc_type == "TodoList") 
        emit(null, doc); 
 }