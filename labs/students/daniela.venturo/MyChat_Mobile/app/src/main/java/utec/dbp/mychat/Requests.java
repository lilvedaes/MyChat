package utec.dbp.mychat;

import android.content.Context;
import android.util.Log;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by dani on 5/28/18.
 */

public class Requests {
    private static final String TAG = "Requests";
    public Context mContext;
    public Requests(Context context) {
        mContext = context;
    }

    public void login(final String username,final String password, final VolleyCallback callback) {
        String url = "http://10.0.2.2:5000/dologin";

        StringRequest stringRequest = new StringRequest(Request.Method.POST, url, new Response.Listener<String>(){

            @Override
            public void onResponse(String response) {
                try {
                    callback.onSuccess(response);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                callback.onFailure(error.toString());
            }
        }){
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String,String> params = new HashMap<>();
                params.put("User-Agent","android");
                params.put("Content-Type","application/x-www-form-urlencoded");
                return params;
            }

            @Override
            protected Map<String, String> getParams() throws AuthFailureError {
                HashMap<String,String> params = new HashMap<>();
                params.put("username", username);
                params.put("password",password);
                return params;
            }
        };
        AllTheSingleLadies.getInstance(mContext).addToRequestQueue(stringRequest);
    }

    public interface VolleyCallback {
        void onSuccess(String resp) throws JSONException;
        void onFailure(String error);
    }
}
