package com.example.ess;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.Volley;
import com.example.ess.Classes.API;
import com.example.ess.Classes.Preferences;
import com.squareup.picasso.Picasso;

import org.json.JSONArray;
import org.json.JSONException;

public class ServiceBranchDetailsActivity extends AppCompatActivity {

    private Button btnAdd;
    private ImageView logo;
    private TextView branchLocation, branchNumber, branchAddress,
            departmentNumber, departmentLink, departmentAddress, departmentDesc;

    String id = "", mapLink = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_service_branch_details);

        Intent project = getIntent();
        id = project.getStringExtra("id");

        btnAdd = (Button) this.findViewById(R.id.btnAdd);
        logo = (ImageView) this.findViewById(R.id.logo);

        branchLocation = (TextView) this.findViewById(R.id.branchLocation);
        branchNumber = (TextView) this.findViewById(R.id.branchNumber);
        branchAddress = (TextView) this.findViewById(R.id.branchAddress);
        departmentNumber = (TextView) this.findViewById(R.id.departmentNumber);
        departmentLink = (TextView) this.findViewById(R.id.departmentLink);
        departmentAddress = (TextView) this.findViewById(R.id.departmentAddress);
        departmentDesc = (TextView) this.findViewById(R.id.departmentDesc);

        showDetails();

        branchNumber.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                String number = branchNumber.getText().toString();
                makeCall(number);

            }
        });

        departmentNumber.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                String number = departmentNumber.getText().toString();
                makeCall(number);

            }
        });

        departmentLink.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                String link = departmentLink.getText().toString();
                openBrowser(link);

            }
        });

        branchAddress.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                if (!mapLink.equals("")) {
                    openBrowser(mapLink);
                }

            }
        });

    }

    //    Function for show department branch details
    private void showDetails() {

        String URL = API.BRANCHES_API + "/" + id;

        RequestQueue requestQueue = Volley.newRequestQueue(ServiceBranchDetailsActivity.this);
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

                                String strLogo = API.ASSERT_URL + "/" +  (String) responseData.get(10);
                                String bLocation = (String) responseData.get(3);
                                String bNumber = (String) responseData.get(4);
                                String bAddress = (String) responseData.get(5);
                                String dNumber = (String) responseData.get(6);
                                String dLink = (String) responseData.get(7);
                                String dAddress = (String) responseData.get(8);
                                String dDesc = (String) responseData.get(9);
                                String dMapLink = (String) responseData.get(11);

                                mapLink = dMapLink;

                                branchLocation.setText(bLocation);
                                branchNumber.setText(bNumber);
                                branchAddress.setText(bAddress);
                                departmentNumber.setText(dNumber);
                                departmentLink.setText(dLink);
                                departmentAddress.setText(dAddress);
                                departmentDesc.setText(dDesc);

                                Uri imgUri = Uri.parse(strLogo);
                                Picasso.get().load(imgUri).into(logo);

                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(ServiceBranchDetailsActivity.this, error.toString(),Toast.LENGTH_SHORT).show();
                    }
                }

        );

        requestQueue.add(jsonArrayRequest);

    }

//    Method for make phone call
    private void makeCall(String number)
    {
        Intent callIntent = new Intent(Intent.ACTION_DIAL);
        callIntent.setData(Uri.parse("tel:"+number));
        startActivity(callIntent);
    }

    private void openBrowser(String link)
    {
        Intent defaultBrowser = Intent.makeMainSelectorActivity(Intent.ACTION_MAIN, Intent.CATEGORY_APP_BROWSER);
        defaultBrowser.setData(Uri.parse(link));
        startActivity(defaultBrowser);
    }

}