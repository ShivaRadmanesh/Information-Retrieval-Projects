/*
 * Indexer.java
 *
 * Created on 6 March 2006, 13:05
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.apache;

import org.apache.*;
import java.io.IOException;
import java.io.StringReader;
import java.nio.file.Path;
import java.io.File;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.*;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
//import org.apache.http.impl.conn.Wire;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;



/**
 *
 * @author John
 */
public class Indexer {

   int groupNum;
    Directory indexDir = null;

    /** Creates a new instance of Indexer */
    public Indexer() {
    }

    private IndexWriter indexWriter = null;

    public IndexWriter getIndexWriter(boolean create) throws IOException {
        if (indexWriter == null) {
            indexDir = FSDirectory.open(Path.of("luceneIndexer/index_directory"));
            IndexWriterConfig config = new IndexWriterConfig(new StandardAnalyzer());
            // iwc.setOpenMode(OpenMode.CREATE_OR_APPEND);
            indexWriter = new IndexWriter(indexDir, config);
        }
        return indexWriter;
   }

    public void closeIndexWriter() throws IOException {
        if (indexWriter != null) {
            indexWriter.close();
        }
   }
    

    public void indexDoc(String docContent, int docNum) throws IOException {

        System.out.println("Indexing document: " + docNum);
        IndexWriter writer = getIndexWriter(false);
        Document doc = new Document();
        doc.add(new StringField("document_number", String.valueOf(docNum), Field.Store.YES));
        doc.add(new TextField("content", docContent, Field.Store.YES));
        writer.addDocument(doc);
    }   
    

    public String[] rebuildIndexes(String[] docs, int docCount, int groupNum) throws IOException {
          getIndexWriter(true);
          //
          // Index all Accommodation entries
          //
          int startDocNum = (groupNum - 1) * docCount + 1;
          for(int i = 0; i < docs.length; i++) {
              indexDoc(docs[i], startDocNum + i);              
          }

          String[] indexDirContent = indexDir.listAll();
          closeIndexWriter();
          
          return indexDirContent;
     }    
}
