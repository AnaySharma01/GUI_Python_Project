//Imports libraries
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

class LoginPage extends JFrame {
    private JLabel password, label;
    private JTextField username;
    private JButton button;
    private JPasswordField password1;

    public LoginPage()
    {
        //Creates login page
        super("Login");

        //Creates new panel
        JPanel panel = new JPanel();
        panel.setLayout(null);
        this.add(panel);
        //Creates username label
        label = new JLabel("Username");
        label.setBounds(100, 8, 70, 20);
        panel.add(label);
        //Creates username input box
        username = new JTextField();
        username.setBounds(100, 27, 193, 28);
        panel.add(username);
        //Creates password label
        password = new JLabel("Password");
        password.setBounds(100, 55, 70, 20);
        panel.add(password);
        //Creates password input box
        password1 = new JPasswordField();
        password1.setBounds(100, 75, 193, 28);
        panel.add(password1);
        //Creates login button
        button = new JButton("Login");
        button.setBounds(100, 110, 90, 25);
        button.setBackground(Color.PINK);
        panel.add(button);
        //Gets username and password once login button clicked
        button.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String usrname = username.getText();
                String paswrd = String.valueOf(password1.getPassword());
                authenticate(usrname,paswrd);
            }
        });
    }
    private boolean authenticate(String username, String password) {
        //Checks password
        if("a".equals(username) && "a".equals(password))
        {
            JOptionPane.showMessageDialog(null, "Login Successful");
            this.dispose();
            JavaClient.showMain();
            return true;
        }
        else
        {
            JOptionPane.showMessageDialog(null, "Username or Password mismatch ");
            return false;
        }

    }
    public static void main(String[] args) {
        //Creates a new client
        LoginPage app = new LoginPage();
        //Sets the client settings
        app.setSize(400, 300);
        app.setVisible(true);
        app.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        app.setLocationRelativeTo(null);
    }
}
