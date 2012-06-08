function(doc) {
    if (doc.doc_type == "Todo")
        emit(doc._id, doc);
 }