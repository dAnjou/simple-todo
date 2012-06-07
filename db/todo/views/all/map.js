function(doc) { 
    if (doc.doc_type == "Todo") 
        emit(null, doc); 
 }