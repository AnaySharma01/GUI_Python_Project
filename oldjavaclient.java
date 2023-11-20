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
    public static void main(String[] args) {
        //Creates a new client
        JavaClient app = new JavaClient();
        //Sets the client settings
        app.setSize(600, 600);
        app.setVisible(true);
        app.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        app.setLocationRelativeTo(null);
    }
}
