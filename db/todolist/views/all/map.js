function(doc) {
    if (doc.doc_type == "TodoList")
        emit(doc._id, doc);
 }