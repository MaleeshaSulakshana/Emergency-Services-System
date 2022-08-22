package com.example.ess;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
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

import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;

public class SignUpActivity extends AppCompatActivity {

    private TextView textLogin;
    private EditText fname, lname, email, nic, number, address;
    private Button btnSignUp;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_up);

        textLogin = (TextView) this.findViewById(R.id.textLogin);

        fname = (EditText) this.findViewById(R.id.fname);
        lname = (EditText) this.findViewById(R.id.lname);
        email = (EditText) this.findViewById(R.id.email);
        nic = (EditText) this.findViewById(R.id.nic);
        number = (EditText) this.findViewById(R.id.number);
        address = (EditText) this.findViewById(R.id.address);

        btnSignUp = (Button) this.findViewById(R.id.btnSignUp);

        textLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(SignUpActivity.this, SignInActivity.class);
                startActivity(intent);
            }
        });

        btnSignUp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                signUp();

            }
        });

    }

    private void signUp() {

        String fnameValue = fname.getText().toString();
        String lnameValue = lname.getText().toString();
        String emailValue = email.getText().toString();
        String nicValue = nic.getText().toString();
        String numberValue = number.getText().toString();
        String addressValue = address.getText().toString();

        if (fnameValue.equals("") || lnameValue.equals("") || nicValue.equals("") || numberValue.equals("") ||
                emailValue.equals("") || addressValue.equals("")) {
            Toast.makeText(SignUpActivity.this, "Fields empty!",Toast.LENGTH_SHORT).show();

        } else if (number.length() != 10) {
            Toast.makeText(SignUpActivity.this, "Invalid mobile number!",Toast.LENGTH_SHORT).show();

        } else {

            try {
                String URL = API.USER_API + "/register";

                RequestQueue requestQueue = Volley.newRequestQueue(SignUpActivity.this);
                JSONObject jsonBody = new JSONObject();

                jsonBody.put("first_name", fnameValue);
                jsonBody.put("last_name", lnameValue);
                jsonBody.put("email", emailValue);
                jsonBody.put("nic", nicValue);
                jsonBody.put("number", numberValue);
                jsonBody.put("address", addressValue);

                final String requestBody = jsonBody.toString();

                StringRequest stringRequest = new StringRequest(Request.Method.POST, URL, new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {

                        try {
                            JSONObject jsonObject = new JSONObject(response);

                            String status = jsonObject.getString("status");
                            String msg = jsonObject.getString("msg");

                            if (status.equals("success")) {
                                fname.setText("");
                                lname.setText("");
                                email.setText("");
                                nic.setText("");
                                number.setText("");
                                address.setText("");
                            }

                            Toast.makeText(SignUpActivity.this, msg, Toast.LENGTH_SHORT).show();

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {

                        Toast.makeText(SignUpActivity.this, "Some error occur" + error.toString(), Toast.LENGTH_SHORT).show();
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