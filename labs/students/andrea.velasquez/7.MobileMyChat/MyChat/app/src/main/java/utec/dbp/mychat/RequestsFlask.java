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

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class RequestsFlask {
    private static final String TAG = "RequestsFlask";
    public Context mContext;
    public RequestsFlask(Context context) {
        mContext = context;
    }

    public interface VolleyCallback {
        void onSuccess(String resp);
        void onFailure(String error);
    }

    public void login(final String username,final String password, final VolleyCallback callback) {
        String url = "http://10.0.2.2:5000/dologin";

        StringRequest stringRequest = new StringRequest(Request.Method.POST, url, new Response.Listener<String>(){

            @Override
            public void onResponse(String response) {
                callback.onSuccess(response);
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
        Singleton.getInstance(mContext).addToRequestQueue(stringRequest);
    }
}