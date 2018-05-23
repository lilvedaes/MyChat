package utec.dbp.mychat;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;
import com.google.gson.Gson;

import utec.dbp.mychat.entities.User;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void onClickBtnLogin(View v)
    {

        EditText txtUsername   = (EditText)findViewById(R.id.txtUsername);
        EditText txtPassword   = (EditText)findViewById(R.id.txtPassword);
        User user = new User();
        user.setUsername(txtUsername.getText().toString());
        user.setPassword(txtPassword.getText().toString());

        Toast.makeText(this, new Gson().toJson(user), Toast.LENGTH_LONG).show();
        //Toast.makeText(this, "Clicked on Button"+txtUsername.getText()+" - "+txtPassword.getText(), Toast.LENGTH_LONG).show();
    }
}
