package com.example.ess;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class AddInquiryActivity extends AppCompatActivity {

    private Button btnAdd, btnSelectImages, btnSelectVideo;
    private EditText details, location, contact;
    private TextView imageCount, videoCount;

    private String id = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_inquiry);

        Intent intentThis = getIntent();
        id = intentThis.getStringExtra("id");

        btnAdd = (Button) this.findViewById(R.id.btnAdd);
        btnSelectImages = (Button) this.findViewById(R.id.btnSelectImages);
        btnSelectVideo = (Button) this.findViewById(R.id.btnSelectVideo);

        details = (EditText) this.findViewById(R.id.details);
        location = (EditText) this.findViewById(R.id.location);
        contact = (EditText) this.findViewById(R.id.contact);

        imageCount = (TextView) this.findViewById(R.id.imageCount);
        videoCount = (TextView) this.findViewById(R.id.videoCount);

    }
}