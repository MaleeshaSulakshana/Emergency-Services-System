package com.example.ess;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;

public class DashboardActivity extends AppCompatActivity {

    private LinearLayout btnServices, btnInquiries, btnProfile;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dashboard);

        btnServices = (LinearLayout) this.findViewById(R.id.btnServices);
        btnInquiries = (LinearLayout) this.findViewById(R.id.btnInquiries);
        btnProfile = (LinearLayout) this.findViewById(R.id.btnProfile);

        btnServices.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent intent = new Intent(DashboardActivity.this, ServicesActivity.class);
                startActivity(intent);

            }
        });

        btnInquiries.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent intent = new Intent(DashboardActivity.this, InquiriesActivity.class);
                startActivity(intent);

            }
        });

        btnProfile.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent intent = new Intent(DashboardActivity.this, ProfileActivity.class);
                startActivity(intent);

            }
        });


    }
}