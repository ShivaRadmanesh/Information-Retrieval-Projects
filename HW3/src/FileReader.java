import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;
import java.io.File;

public class FileReader {
    private int group_id;
    private int start_id;
    private int end_id;

    public static  void main(String args[]){
        FileReader fileReader = new FileReader();
        ArrayList<String> output = fileReader.read("lucene_ dataset.txt");
        System.out.println(output);
    }
    public FileReader(){
        System.out.print("Please enter your group number:");
        Scanner input = new Scanner(System.in);
        group_id = input.nextInt();
        start_id = (group_id-1)*103+1;
        end_id = group_id*103;
        System.out.println("Your first document's id is :"+start_id);
        System.out.println("Your last document's id is :"+end_id);
    }

    public ArrayList<String> read(String path){
        ArrayList<String> output = new ArrayList<>();
        try {
            File file = new File(path);
            Scanner scanner = new Scanner(file);

            boolean started = false;
            String currentDoc = "";

            while (scanner.hasNextLine()) {
                String data = scanner.nextLine();

                if(started && !data.equals(".W")){
                    currentDoc = currentDoc + data;
                }
                if(data.equals(".I "+start_id))
                    started=true;
                if (data.equals(".I "+(end_id+1)))
                {
                    output.add(currentDoc);
                    break;
                }
                if (data.equals(".W") && started) {
                    output.add(currentDoc);
                    currentDoc = "";
                }
            }
            scanner.close();
        } catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
        output.remove(0);
        return output;
    }
}
