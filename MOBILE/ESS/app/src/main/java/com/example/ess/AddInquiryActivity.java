package com.example.ess;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
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
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.example.ess.Classes.API;
import com.example.ess.Classes.Preferences;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.Console;
import java.io.File;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.HashMap;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;

public class AddInquiryActivity extends AppCompatActivity {

    private Button btnAdd, btnSelectImages, btnSelectVideo;
    private EditText details, location, contact;
    private TextView imageCount, videoCount;

    private String id = "";

    private static final int PICK_IMAGE = 100;
    private static final int REQUEST_TAKE_GALLERY_VIDEO = 3;
    private Uri imageUri = Uri.EMPTY;
    private ArrayList<Bitmap> bitmapList = new ArrayList<Bitmap>();
    private String videoPath = "";

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

        btnSelectImages.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                openGalleryForSelectImages();

            }
        });

        btnSelectVideo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                openGalleryForSelectVideo();

            }
        });

        btnAdd.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                String strDetails = details.getText().toString();
                String strLocation = location.getText().toString();
                String strContact = contact.getText().toString();

                if (strDetails.equals("") || strContact.equals("") || strLocation.equals("")) {
                    Toast.makeText(AddInquiryActivity.this, "Fields are empty!",Toast.LENGTH_SHORT).show();

                } else if (bitmapList.size() == 0) {
                    Toast.makeText(AddInquiryActivity.this, "Please add one or more images for proof.",Toast.LENGTH_SHORT).show();

                } else {

                    try {
                        String URL = API.INQUIRIES_API + "/add_inquiry";

                        JSONArray jsonArray = new JSONArray();
                        for (int i=0; i < bitmapList.size(); i++) {
                            JSONObject jsonBody = new JSONObject();
                            String image = getStringImage(bitmapList.get(i));
                            jsonBody.put("image", image);
                            jsonArray.put(jsonBody);
                        }

                        JSONObject parameter =  new JSONObject();
                        parameter.put("images", jsonArray);
                        parameter.put("details", strDetails);
                        parameter.put("location", strLocation);
                        parameter.put("contact", strContact);
                        parameter.put("user_id", Preferences.LOGGED_USER_ID);
                        parameter.put("branch", id);
                        parameter.put("lat", "87.215");
                        parameter.put("lon", "127.5246");

//                        if (!videoPath.equals("")) {
////                            File file = new File(videoPath);
//                            File videoFile = new File(videoPath);
//                            RequestBody videoBody = RequestBody.create(MediaType.parse("video/*"), videoFile);
//                            MultipartBody.Part vFile = MultipartBody.Part.createFormData("video", videoFile.getName(), videoBody);
//                            parameter.put("video", vFile);
//
//                        }

                        JsonObjectRequest jsonObject = new JsonObjectRequest(Request.Method.POST, URL, parameter, new Response.Listener<JSONObject>() {
                            @Override
                            public void onResponse(JSONObject response) {

                                try {

                                    String status = response.getString("status");
                                    String msg = response.getString("msg");

                                    Toast.makeText(AddInquiryActivity.this, msg, Toast.LENGTH_SHORT).show();

                                    if (status.equals("success")) {
                                        Intent intent = new Intent(AddInquiryActivity.this, InquiriesActivity.class);
                                        startActivity(intent);
                                        finish();
                                    }

                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }

                            }
                        }, new Response.ErrorListener() {
                            @Override
                            public void onErrorResponse(VolleyError error) {
                                Toast.makeText(AddInquiryActivity.this, error.getMessage().toString(), Toast.LENGTH_SHORT).show();
                            }
                        });


                        RequestQueue queue = Volley.newRequestQueue(AddInquiryActivity.this);
                        queue.add(jsonObject);

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                }

            }
        });

    }

    private void openGalleryForSelectVideo()
    {
        Intent intent = new Intent();
        intent.setType("video/*");
        intent.putExtra(Intent.ACTION_PICK, true);
        intent.setAction(Intent.ACTION_GET_CONTENT);
        startActivityForResult(Intent.createChooser(intent,"Select Video"), REQUEST_TAKE_GALLERY_VIDEO);
    }

    private void openGalleryForSelectImages()
    {
        Intent intent = new Intent();
        intent.setType("image/*");
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
        intent.setAction(Intent.ACTION_GET_CONTENT);
        startActivityForResult(Intent.createChooser(intent,"Select Images"), PICK_IMAGE);
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == RESULT_OK) {
            if (requestCode == PICK_IMAGE) {
                if (data.getClipData() != null) {
                    int count = data.getClipData().getItemCount();
                    for (int i = 0; i < count; i++) {
                        try {
                            Uri imageUri = data.getClipData().getItemAt(i).getUri();
                            Bitmap bitmap = (Bitmap) MediaStore.Images.Media.getBitmap(getContentResolver(), imageUri);
                            bitmapList.add(bitmap);
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                    imageCount.setText(String.valueOf(count) + " Images selected");
                }
            } else {

                Uri videoUri = data.getData();
                String selectedVideoPAth = getPath(videoUri);
                if (selectedVideoPAth != null) {
                    videoPath = selectedVideoPAth;
                    videoCount.setText("1 Video selected");
                }

            }
        }
    }

    public String getPath(Uri uri) {
        String[] projection = { MediaStore.Video.Media.DATA };
        Cursor cursor = getContentResolver().query(uri, projection, null, null, null);
        if (cursor != null) {
            int column_index = cursor
                    .getColumnIndexOrThrow(MediaStore.Video.Media.DATA);
            cursor.moveToFirst();
            return cursor.getString(column_index);
        } else
            return null;
    }

    public String getStringImage(Bitmap bmp) {
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        bmp.compress(Bitmap.CompressFormat.JPEG, 100, byteArrayOutputStream);
        byte[] imageBytes = byteArrayOutputStream.toByteArray();
        String encodedImage = Base64.encodeToString(imageBytes, Base64.DEFAULT);
        return encodedImage;
    }

}