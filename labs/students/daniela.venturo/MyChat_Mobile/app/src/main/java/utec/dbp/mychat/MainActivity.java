package utec.dbp.mychat;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import utec.dbp.mychat.entities.User;

public class MainActivity extends AppCompatActivity {
    Requests rq = new Requests(this);
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

        rq.login(user.getUsername(), user.getPassword(), new Requests.VolleyCallback() {
            @Override
            public void onSuccess(String resp) throws JSONException {
                if (resp.equals("ok")){
                    Intent myIntent = new Intent(MainActivity.this, chatScreen.class);
                    MainActivity.this.startActivity(myIntent);
                }
                else {
                    Toast.makeText(MainActivity.this, resp, Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(String error) {
            }
        });
    }
}
