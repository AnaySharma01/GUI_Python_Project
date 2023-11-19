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


    private JButton forwardBtn = new BasicArrowButton(BasicArrowButton.NORTH);
    private JButton leftBtn = new BasicArrowButton(BasicArrowButton.WEST);
    private JButton rightBtn = new BasicArrowButton(BasicArrowButton.EAST);
    private JButton backBtn = new BasicArrowButton(BasicArrowButton.SOUTH);


    private JTextField textTurn = new JTextField("0");
    private JTextField textTime = new JTextField("0");
    private JLabel resultText = new JLabel("");


    public JavaClient() {
        super("JavaClient");


        this.add(resultText, BorderLayout.NORTH);


        JPanel buttonPanel = new JPanel();
        this.add(buttonPanel, BorderLayout.CENTER);
        buttonPanel.setLayout(new GridLayout(5, 3));
        buttonPanel.add(new JPanel());
        buttonPanel.add(new JPanel());
        buttonPanel.add(new JPanel());


        buttonPanel.add(new JPanel());
        buttonPanel.add(forwardBtn);
        buttonPanel.add(new JPanel());


        buttonPanel.add(leftBtn);
        buttonPanel.add(new JPanel());
        buttonPanel.add(rightBtn);


        buttonPanel.add(new JPanel());
        buttonPanel.add(backBtn);
        buttonPanel.add(new JPanel());


        buttonPanel.add(new JPanel());
        buttonPanel.add(new JPanel());
        buttonPanel.add(new JPanel());




        JPanel textPanel = new JPanel();
        textPanel.setBorder(new EmptyBorder(10, 10, 10, 10));
        this.add(textPanel, BorderLayout.SOUTH);
        textPanel.setLayout(new GridLayout(2, 2));
        textPanel.add(new JLabel("Degree Turn:"));
        textPanel.add(textTurn);
        textPanel.add(new JLabel("Time:"));
        textPanel.add(textTime);
        // This method will set adjust the size of the container so it can contain all other controls
        pack();
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
    }




    private String moveRobot(String direction, String turn, String time) {
        // Replace the URL with the actual REST API endpoint
        String apiUrl = "http://127.0.0.1:5000/move?direction=" + direction + "&turn=" + turn + "&time=" + time;
        String returnText = "";
        try {
            // Create a URL object with the API endpoint
            URL url = new URL(apiUrl);


            // Open a connection to the URL
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();


            // Set the request method to GET
            connection.setRequestMethod("GET");


            // Get the response code
            int responseCode = connection.getResponseCode();


            // Check if the request was successful (HTTP 200 OK)
            if (responseCode == HttpURLConnection.HTTP_OK) {


                // Read the response from the input stream
                BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                String line;
                StringBuilder response = new StringBuilder();


                while ((line = reader.readLine()) != null) {
                    response.append(line);
                }
                // Close the reader
                reader.close();
                if ("\"success\"".equals(response.toString())) {
                    returnText = "Robot Moved Parameters: Direction-" + direction + " Time-" + time + " seconds Turn-"+turn +" degrees";
                }
            } else {
                // Print an error message if the request was not successful
                returnText = "Error: " + responseCode;
            }


            // Close the connection
            connection.disconnect();


        } catch (Exception e) {
            e.printStackTrace();
        }
        return returnText;
    }


    public static void main(String[] args) {
        JavaClient app = new JavaClient();
        app.setSize(600, 600);
        app.setVisible(true);
        app.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        app.setLocationRelativeTo(null);
    }
}
