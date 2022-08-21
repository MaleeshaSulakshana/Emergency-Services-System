package com.example.ess;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;

import com.example.ess.Classes.Preferences;

public class DashboardActivity extends AppCompatActivity {

    private LinearLayout btnServices, btnSearch, btnInquiries, btnProfile, btnLogout;

    private SharedPreferences sharedPreferences;
    private SharedPreferences.Editor editor;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dashboard);

        btnServices = (LinearLayout) this.findViewById(R.id.btnServices);
        btnSearch = (LinearLayout) this.findViewById(R.id.btnSearch);
        btnInquiries = (LinearLayout) this.findViewById(R.id.btnInquiries);
        btnProfile = (LinearLayout) this.findViewById(R.id.btnProfile);
        btnLogout = (LinearLayout) this.findViewById(R.id.btnLogout);

//        For shared preferences
        sharedPreferences = getSharedPreferences("Login", MODE_PRIVATE);
        editor = sharedPreferences.edit();

        btnServices.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent intent = new Intent(DashboardActivity.this, ServicesActivity.class);
                startActivity(intent);

            }
        });

        btnSearch.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent intent = new Intent(DashboardActivity.this, SearchActivity.class);
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

        btnLogout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Preferences.LOGGED_USER_ID = "";
                Preferences.LOGGED_USER_NAME = "";

                editor.clear();
                editor.apply();

                Intent intent = new Intent(DashboardActivity.this, MainActivity.class);
                startActivity(intent);
                finishAffinity();

            }
        });

    }
}