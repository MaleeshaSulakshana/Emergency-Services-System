package com.example.ess;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
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
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.example.ess.Classes.API;
import com.example.ess.Classes.Preferences;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;

public class ProfileActivity extends AppCompatActivity {

    private TextView textPswChange;
    private EditText fname, lname, email, nic, number, address;
    private Button btnUpdate;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);

        textPswChange = (TextView) this.findViewById(R.id.textPswChange);

        fname = (EditText) this.findViewById(R.id.fname);
        lname = (EditText) this.findViewById(R.id.lname);
        email = (EditText) this.findViewById(R.id.email);
        nic = (EditText) this.findViewById(R.id.nic);
        number = (EditText) this.findViewById(R.id.number);
        address = (EditText) this.findViewById(R.id.address);

        btnUpdate = (Button) this.findViewById(R.id.btnUpdate);

        getProfileData();

        textPswChange.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent intent = new Intent(ProfileActivity.this, PswChangeActivity.class);
                startActivity(intent);

            }
        });

        btnUpdate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                updateProfile();

            }
        });


    }

//    Function for get profile details
    private void getProfileData() {

        String URL = API.USER_API + "/" + Preferences.LOGGED_USER_ID;

        RequestQueue requestQueue = Volley.newRequestQueue(ProfileActivity.this);
        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(
                Request.Method.GET,
                URL,
                null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {

                        try {

                            if (response.length() > 0) {

                                JSONArray responseData = response.getJSONArray(0);

                                Integer id = (Integer) responseData.get(0);
                                String firstName = (String) responseData.get(1);
                                String lastName = (String) responseData.get(2);
                                String Email = (String) responseData.get(3);
                                String NIC = (String) responseData.get(4);
                                String Number = (String) responseData.get(5);
                                String Address = (String) responseData.get(6);

                                fname.setText(firstName);
                                lname.setText(lastName);
                                email.setText(Email);
                                nic.setText(NIC);
                                number.setText(Number);
                                address.setText(Address);

                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(ProfileActivity.this, error.toString(),Toast.LENGTH_SHORT).show();
                    }
                }

        );

        requestQueue.add(jsonArrayRequest);

    }

    private void updateProfile() {

        String idValue = Preferences.LOGGED_USER_ID;
        String fnameValue = fname.getText().toString();
        String lnameValue = lname.getText().toString();
        String emailValue = email.getText().toString();
        String nicValue = nic.getText().toString();
        String numberValue = number.getText().toString();
        String addressValue = address.getText().toString();

        if (fnameValue.equals("") || lnameValue.equals("") || nicValue.equals("") || numberValue.equals("") ||
                emailValue.equals("") || addressValue.equals("")) {

            Toast.makeText(ProfileActivity.this, "Fields empty!", Toast.LENGTH_SHORT).show();

        } else if (numberValue.length() != 10 ) {

            Toast.makeText(ProfileActivity.this, "Invalid mobile number!", Toast.LENGTH_SHORT).show();

        } else {

            try {
                String URL = API.USER_API + "/update";

                RequestQueue requestQueue = Volley.newRequestQueue(ProfileActivity.this);
                JSONObject jsonBody = new JSONObject();
                jsonBody.put("id", idValue);
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

                            Toast.makeText(ProfileActivity.this, msg, Toast.LENGTH_SHORT).show();

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {

                        Toast.makeText(ProfileActivity.this, "Some error occur" + error.toString(), Toast.LENGTH_SHORT).show();
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