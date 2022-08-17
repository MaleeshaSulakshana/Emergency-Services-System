package com.example.ess;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.example.ess.Classes.API;
import com.example.ess.Classes.Preferences;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;

public class SignInActivity extends AppCompatActivity {

    private EditText email, psw;
    private TextView textSignUp;
    private Button btnLogin;

    private SharedPreferences sharedPreferences;
    private SharedPreferences.Editor editor;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_in);

        email = (EditText) this.findViewById(R.id.email);
        psw = (EditText) this.findViewById(R.id.psw);
        textSignUp = (TextView) this.findViewById(R.id.textSignUp);
        btnLogin = (Button) this.findViewById(R.id.btnLogin);

//        For shared preferences
        sharedPreferences = getSharedPreferences("Login", MODE_PRIVATE);
        editor = sharedPreferences.edit();

        textSignUp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent intent = new Intent(SignInActivity.this, SignUpActivity.class);
                startActivity(intent);

            }
        });

        btnLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                signIn();

            }
        });

    }


    private void signIn() {

        String emailValue = email.getText().toString();
        String pswValue = psw.getText().toString();

        if (emailValue.equals("") || pswValue.equals("")) {
            Toast.makeText(SignInActivity.this, "Fields empty!",Toast.LENGTH_SHORT).show();

        } else {

            try {
                String URL = API.USER_API + "/login";

                RequestQueue requestQueue = Volley.newRequestQueue(SignInActivity.this);
                JSONObject jsonBody = new JSONObject();

                jsonBody.put("email", emailValue);
                jsonBody.put("psw", pswValue);

                final String requestBody = jsonBody.toString();

                StringRequest stringRequest = new StringRequest(Request.Method.POST, URL, new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {

                        try {
                            JSONObject jsonObject = new JSONObject(response);

                            String status = jsonObject.getString("status");
                            String msg = jsonObject.getString("msg");

                            if (status.equals("success")) {

                                email.setText("");
                                psw.setText("");

                                String id = jsonObject.getString("id");
                                String name = jsonObject.getString("name");

                                Preferences.LOGGED_USER_ID = id;
                                Preferences.LOGGED_USER_NAME = name;

                                editor.putString("id", id );
                                editor.putString("name", name );
                                editor.commit();

                                Intent intent = new Intent(SignInActivity.this, DashboardActivity.class);
                                startActivity(intent);
                                finish();

                            }

                            Toast.makeText(SignInActivity.this, msg, Toast.LENGTH_SHORT).show();

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {

                        Toast.makeText(SignInActivity.this, "Some error occur" + error.toString(), Toast.LENGTH_SHORT).show();
                    }
                }) {
                    @Override
                    public String getBodyContentType() {
                        return "application/json; charset=utf-8";
                    }

                    @Override
                    public byte[] getBody() throws AuthFailureError {
                        try {
                            return requestBody == null ? null : requestBody.getBytes("utf-8");
                        } catch (UnsupportedEncodingException uee) {
                            return null;
                        }
                    }
                };

                requestQueue.add(stringRequest);
            } catch (JSONException e) {
                e.printStackTrace();
            }

        }

    }

}