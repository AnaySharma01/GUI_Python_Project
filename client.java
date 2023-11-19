import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class Main extends JFrame {

    private static final String SERVER_URL = "http://192.168.1.28:4444";

    public Main() {
        setTitle("Robot Controller");
        setSize(300, 200);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Create buttons with arrow symbols
        JButton forwardButton = new JButton("\u2191"); // Up arrow
        JButton backwardButton = new JButton("\u2193"); // Down arrow
        JButton leftButton = new JButton("\u2190"); // Left arrow
        JButton rightButton = new JButton("\u2192"); // Right arrow
        JButton stopButton = new JButton("Stop");

        // Create a panel with a GridLayout
        JPanel panel = new JPanel(new GridLayout(3, 3));

        // Add empty labels for layout purposes
        panel.add(new JLabel());
        panel.add(forwardButton);
        panel.add(new JLabel());
        panel.add(leftButton);
        panel.add(stopButton);
        panel.add(rightButton);
        panel.add(new JLabel());
        panel.add(backwardButton);
        panel.add(new JLabel());

        // Add action listeners to buttons
        forwardButton.addActionListener(new ButtonClickListener("/forward"));
        backwardButton.addActionListener(new ButtonClickListener("/backward"));
        leftButton.addActionListener(new ButtonClickListener("/left"));
        rightButton.addActionListener(new ButtonClickListener("/right"));
        stopButton.addActionListener(new ButtonClickListener("/stop"));

        getContentPane().add(panel);
        setVisible(true);
    }

    private class ButtonClickListener implements ActionListener {
        private String endpoint;

        public ButtonClickListener(String endpoint) {
            this.endpoint = endpoint;
        }

        @Override
        public void actionPerformed(ActionEvent e) {
            sendRequest(endpoint);
        }
    }

    private void sendRequest(String endpoint) {
        try {
            URL url = new URL(SERVER_URL + endpoint);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");

            int responseCode = connection.getResponseCode();
            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String line;
            StringBuilder response = new StringBuilder();

            while ((line = reader.readLine()) != null) {
                response.append(line);
            }

            reader.close();
            connection.disconnect();

            System.out.println("Response Code: " + responseCode);
            System.out.println("Response Content: " + response.toString());
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Main());
    }
}

