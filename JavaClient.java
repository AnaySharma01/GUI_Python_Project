//Imports libraries
import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.plaf.basic.BasicArrowButton;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class JavaClient extends JFrame {

    //Server url for rest api server
    private static final String SERVER_URL = "http://192.168.1.17:4444/";
    //Creates arrow buttons
    private JButton forwardBtn = new BasicArrowButton(BasicArrowButton.NORTH);
    private JButton leftBtn = new BasicArrowButton(BasicArrowButton.WEST);
    private JButton rightBtn = new BasicArrowButton(BasicArrowButton.EAST);
    private JButton backBtn = new BasicArrowButton(BasicArrowButton.SOUTH);
    private JButton stopBtn = new JButton("Stop");
    private JButton startBtn = new JButton("Start");

    //Creates input boxes
    private JTextField textTurn = new JTextField("0");
    private JTextField textTime = new JTextField("0");
    private JLabel resultText = new JLabel("");
    public JavaClient() {
        //Adds title
        super("JavaClient");
        // Set background color for Start button to green and Stop button to red
        startBtn.setBackground(Color.GREEN);
        stopBtn.setBackground(Color.RED);

        //Grids buttons
        this.add(resultText, BorderLayout.NORTH);
        JPanel buttonPanel = new JPanel();
        this.add(buttonPanel, BorderLayout.CENTER);
        buttonPanel.setLayout(new GridLayout(5, 5));
        buttonPanel.add(new JPanel());
        buttonPanel.add(new JPanel());
        buttonPanel.add(forwardBtn);
        buttonPanel.add(new JPanel());
        buttonPanel.add(new JPanel());

        buttonPanel.add(new JPanel());
        buttonPanel.add(new JPanel());
        buttonPanel.add(startBtn);
        buttonPanel.add(new JPanel());
        buttonPanel.add(new JPanel());

        buttonPanel.add(leftBtn);
        buttonPanel.add(new JPanel());
        buttonPanel.add(new JPanel());
        buttonPanel.add(new JPanel());
        buttonPanel.add(rightBtn);

        buttonPanel.add(new JPanel());
        buttonPanel.add(new JPanel());
        buttonPanel.add(stopBtn);
        buttonPanel.add(new JPanel());
        buttonPanel.add(new JPanel());

        buttonPanel.add(new JPanel());
        buttonPanel.add(new JPanel());
        buttonPanel.add(backBtn);
        buttonPanel.add(new JPanel());
        buttonPanel.add(new JPanel());

        //Grids input boxes
        JPanel textPanel = new JPanel();
        textPanel.setBorder(new EmptyBorder(10, 10, 10, 10));
        this.add(textPanel, BorderLayout.SOUTH);
        textPanel.setLayout(new GridLayout(2, 2));
        textPanel.add(new JLabel("Degree Turn:"));
        textPanel.add(textTurn);
        textPanel.add(new JLabel("Time:"));
        textPanel.add(textTime);
        pack();

        //Calls movement functions for buttons from client
        forwardBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                resultText.setText(moveRobot("forward", textTurn.getText(), textTime.getText()));
            }
        });
        backBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                resultText.setText(moveRobot("backward", textTurn.getText(), textTime.getText()));
            }
        });
        leftBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                resultText.setText(moveRobot("left", textTurn.getText(), textTime.getText()));
            }
        });
        rightBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                resultText.setText(moveRobot("right", textTurn.getText(), textTime.getText()));
            }
        });
        stopBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                resultText.setText(moveRobot("stop","",""));
            }
        });
    }
    private String moveRobot(String direction, String turn, String time) {
        //Sets the url for client
        String apiUrl = SERVER_URL + "move?direction=" + direction + "&turn=" + turn + "&time=" + time;
        String returnText = "";
        try {
            // Creates a URL object with the API endpoint
            URL url = new URL(apiUrl);
            // Opens a connection to the URL
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            //Sets the request method to GET
            connection.setRequestMethod("GET");
            // Gets the response code
            int responseCode = connection.getResponseCode();
            // Checks if the request was successful (HTTP 200 OK)
            if (responseCode == HttpURLConnection.HTTP_OK) {
                // Reads the response from the input stream
                BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                String line;
                StringBuilder response = new StringBuilder();
                while ((line = reader.readLine()) != null) {
                    response.append(line);
                }
                // Closes the reader
                reader.close();
                //If successful
                if ("\"success\"".equals(response.toString())) {
                    returnText = "Robot Moved Parameters: Direction-" + direction + " Time-" + time + " seconds Turn-"+turn +" degrees";
                }
            } else {
                // Prints an error message if the request was not successful
                returnText = "Error: " + responseCode;
            }
            // Closes the connection
            connection.disconnect();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return returnText;
    }
    public static void showMain() {
        //Creates a new client
        JavaClient app = new JavaClient();
        //Sets the client settings
        app.setSize(600, 600);
        app.setVisible(true);
        app.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        app.setLocationRelativeTo(null);
    }
    public static void main(String[] args) {
        //Creates a new client
        JavaClient app = new JavaClient();
        //Sets the client settings
        app.setSize(400, 300);
        app.setVisible(true);
        app.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        app.setLocationRelativeTo(null);
    }
}
