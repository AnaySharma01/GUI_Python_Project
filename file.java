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
        setSize(400, 300); // Adjusted the size for the new grid
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Create buttons with arrow symbols (3 times bigger)
        JButton forwardButton = createArrowButton("\u2191", 3); // Up arrow
        JButton backwardButton = createArrowButton("\u2193", 3); // Down arrow
        JButton leftButton = createArrowButton("\u2190", 3); // Left arrow
        JButton rightButton = createArrowButton("\u2192", 3); // Right arrow
        JButton stopButton = new JButton("Stop");
        JButton startButton = new JButton("Start");

        // Set size for Start and Stop buttons to 50%
        Dimension buttonSize = new Dimension(50, 50);
        startButton.setPreferredSize(buttonSize);
        stopButton.setPreferredSize(buttonSize);

        // Set background color for Start button to green and Stop button to red
        startButton.setBackground(Color.GREEN);
        stopButton.setBackground(Color.RED);

        // Create a panel with a GridLayout
        JPanel panel = new JPanel(new GridLayout(3, 5));

        // Add buttons to the panel at specified positions
        panel.add(new JLabel());    // (1,1)
        panel.add(new JLabel());    // (1,2)
        panel.add(forwardButton);   // (1,3)
        panel.add(new JLabel());    // (1,4)
        panel.add(new JLabel());    // (1,5)
        panel.add(leftButton);      // (2,1)
        panel.add(startButton);     // (2,2)
        panel.add(new JLabel());    // (2,3)
        panel.add(stopButton);      // (2,4) - Moved to the second to the last column
        panel.add(rightButton);     // (2,5)
        panel.add(new JLabel());    // (3,1)
        panel.add(new JLabel());    // (3,2)
        panel.add(backwardButton);  // (3,3)
        panel.add(new JLabel());    // (3,4)
        panel.add(new JLabel());    // (3,5)

        // Add action listeners to buttons
        forwardButton.addActionListener(new ButtonClickListener("/forward"));
        backwardButton.addActionListener(new ButtonClickListener("/backward"));
        leftButton.addActionListener(new ButtonClickListener("/left"));
        rightButton.addActionListener(new ButtonClickListener("/right"));
        stopButton.addActionListener(new ButtonClickListener("/stop"));
        startButton.addActionListener(new ButtonClickListener("/start"));

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

    private JButton createArrowButton(String text, int scaleFactor) {
        JButton button = new JButton(text);
        Font originalFont = button.getFont();
        Font newFont = new Font(originalFont.getName(), originalFont.getStyle(), originalFont.getSize() * scaleFactor);
        button.setFont(newFont);
        return button;
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Main());
    }
}
