import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.*;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.store.RAMDirectory;


public class Search {
    public static void main(String[] args) throws IOException, ParseException {

        // gather all the documents in a list of strings
        String[] documents = docsGetter();

        // 0. Specify the analyzer for tokenizing text.
        //    The same analyzer should be used for indexing and searching
        StandardAnalyzer analyzer = new StandardAnalyzer();

        // 1. create the index
        Directory index = FSDirectory.open(Path.of("index_directory"));
        IndexWriterConfig config = new IndexWriterConfig(analyzer);

        IndexWriter w = new IndexWriter(index, config);

        for (int i = 0; i < documents.length; i++){
            addDoc(w, documents[i], (i + 1));
//            System.out.println("----> \t"+ i);
        }
        w.close();

        // 2. query
        Path queryFilePath = Path.of("luceneIndexer/src/dataset/query.txt");
        String regexPattern = "\\.I\\s\\d{3}\\s\\.W\\s";
        String file = null;

        try {
            file = Files.readString(queryFilePath);
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

        String[] queryDocs = file.split(regexPattern);
        String queryStr = queryDocs[7];
        System.out.println("query string : " + queryStr);

//        Term searchTerm = new Term("content", queryStr)

        // the "title" arg specifies the default field to use
        // when no field is explicitly specified in the query.
        Query q = new QueryParser("content", analyzer).parse(queryStr);

        // 3. search
        int hitsPerPage = 503;
        IndexReader reader = DirectoryReader.open(index);
        IndexSearcher searcher = new IndexSearcher(reader);
        TopDocs docs = searcher.search(q, hitsPerPage);
        ScoreDoc[] hits = docs.scoreDocs;

        // 4. display results
        System.out.println("Found " + hits.length + " hits.");
        ArrayList<Integer> seen = new ArrayList<Integer>();
        for(int i=0;i<hits.length;++i) {
            int docId = hits[i].doc;
            Document d = searcher.doc(docId);

            if (!seen.contains(Integer.parseInt(d.get("docNumber")))){
                seen.add(Integer.parseInt(d.get("docNumber")));
            }
            System.out.println("");
            System.out.println((i + 1) + ". " + d.get("docNumber"));
//            System.out.println(d.get("content"));

            Writer output;
            output = new BufferedWriter(new FileWriter("output.txt", true));
            output.append(d.get("docNumber") + "\n");
            output.close();
        }

        ArrayList<Integer> sr = new ArrayList<>();
        sr.add(21);
        sr.add(22);
        sr.add(550);
        sr.add(534);

        for (int docNum : seen){
            if (sr.contains(docNum))
            System.out.println(docNum);
        }
        // reader can only be closed when there
        // is no need to access the documents any more.
        reader.close();
    }

    private static void addDoc(IndexWriter w, String content, int docNum) throws IOException {
        Document doc = new Document();
//        System.out.println("**********" + docNum);
        doc.add(new TextField("content", content, Field.Store.YES));
        doc.add(new StringField("docNumber", Integer.toString(docNum), Field.Store.YES));
        w.addDocument(doc);
    }


    /**
     This function returns all of the documents in an array list of strings
     */
    public static String[] docsGetter(){
        int docCount = 103;

        String regexPattern = "\\.I\\s\\d+\\s\\.W\\s";
        Path filePath = Path.of("luceneIndexer/src/dataset/doc.txt");
        System.out.println(filePath.toAbsolutePath());

        String file = null;
        try {
            file = Files.readString(filePath);
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

        String[] docs = file.split(regexPattern);
        return docs;
    }
}