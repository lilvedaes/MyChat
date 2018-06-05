package utec.dbp.mychat;
import android.content.Context;

import com.android.volley.RequestQueue;
import com.android.volley.toolbox.JsonRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

public class AllTheSingleLadies {
    private static AllTheSingleLadies mInstance;
    private RequestQueue mRequestQueue;
    private static Context mContext;

    private AllTheSingleLadies(Context context) {
        mContext = context;
        mRequestQueue = getRequestQueue();
    }

    public static synchronized AllTheSingleLadies getInstance(Context context) {
        if ( mInstance == null ) {
            mInstance = new AllTheSingleLadies(context);
        }
        return mInstance;
    }

    public RequestQueue getRequestQueue() {
        if ( mRequestQueue == null ) {
            mRequestQueue = Volley.newRequestQueue(mContext.getApplicationContext());
        }
        return mRequestQueue;
    }

    public <T> void addToRequestQueue(StringRequest req) {
        getRequestQueue().add(req);
    }
}
