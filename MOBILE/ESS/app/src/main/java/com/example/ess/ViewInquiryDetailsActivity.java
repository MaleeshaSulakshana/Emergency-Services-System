package com.example.ess;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Context;
import android.content.Intent;
import android.media.Image;
import android.net.Uri;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
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

import java.util.ArrayList;
import java.util.List;

public class ViewInquiryDetailsActivity extends AppCompatActivity {

    private TextView details, location, contact, departmentBranch, date, status;
    private RecyclerView recyclerview;
    private ArrayList<Images> imagesArrayList = new ArrayList<>();
    private RecyclerView.LayoutManager RecyclerViewLayoutManager;
    private LinearLayoutManager HorizontalLayout;
    private Button btnViewVideo, btnViewActions, btnViewComments;

    String id = "", inquiryVideoUrl = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_inquiry_details);

        Intent project = getIntent();
        id = project.getStringExtra("id");

        details = (TextView) findViewById(R.id.details);
        location = (TextView) findViewById(R.id.location);
        contact = (TextView) findViewById(R.id.contact);
        departmentBranch = (TextView) findViewById(R.id.departmentBranch);
        date = (TextView) findViewById(R.id.date);
        status = (TextView) findViewById(R.id.status);

        btnViewVideo = (Button) findViewById(R.id.btnViewVideo);
        btnViewActions = (Button) findViewById(R.id.btnViewActions);
        btnViewComments = (Button) findViewById(R.id.btnViewComments);

        recyclerview = (RecyclerView) findViewById(R.id.recyclerview);
        RecyclerViewLayoutManager = new LinearLayoutManager(getApplicationContext());

        recyclerview.setLayoutManager(RecyclerViewLayoutManager);
        HorizontalLayout = new LinearLayoutManager(ViewInquiryDetailsActivity.this, LinearLayoutManager.HORIZONTAL, false);
        recyclerview.setLayoutManager(HorizontalLayout);
        recyclerview.setItemAnimator(new DefaultItemAnimator());

        showDetails();
        showImages();
        showVideo();

        btnViewVideo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                if (!inquiryVideoUrl.equals("")) {
                    Intent defaultBrowser = Intent.makeMainSelectorActivity(Intent.ACTION_MAIN, Intent.CATEGORY_APP_BROWSER);
                    defaultBrowser.setData(Uri.parse(inquiryVideoUrl));
                    startActivity(defaultBrowser);
                }

            }
        });

        btnViewActions.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent intent = new Intent(ViewInquiryDetailsActivity.this, ViewInquiryActionsActivity.class);
                intent.putExtra("id", id);
                startActivity(intent);

            }
        });

    }

    private void showDetails() {

        String URL = API.INQUIRIES_API + "/" + id;

        RequestQueue requestQueue = Volley.newRequestQueue(ViewInquiryDetailsActivity.this);
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

                                String strDetails = (String) responseData.get(2);
                                String strLocation = (String) responseData.get(3);
                                String strContact = (String) responseData.get(4);
                                String strDepartment = (String) responseData.get(11);
                                String strBranch = (String) responseData.get(12);
                                String strDate = (String) responseData.get(10);
                                String strStatus = (String) responseData.get(9);
//                                String ProfilePic = API.PROFILE_ASSERT_URL + "/" +  (String) responseData.get(7);

                                details.setText(strDetails);
                                location.setText(strLocation);
                                contact.setText(strContact);
                                date.setText(strDate);
                                status.setText(strStatus);
                                departmentBranch.setText(strDepartment + " - " + strBranch);

                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(ViewInquiryDetailsActivity.this, error.toString(),Toast.LENGTH_SHORT).show();
                    }
                }

        );

        requestQueue.add(jsonArrayRequest);

    }

    private void showImages()
    {
        imagesArrayList.clear();
        recyclerview.setAdapter(null);

        ImagesAdapter imagesAdapter = new ImagesAdapter(imagesArrayList);
        recyclerview.setAdapter(imagesAdapter);

        String URL = API.INQUIRIES_API + "/" + id + "/images";

        RequestQueue requestQueue = Volley.newRequestQueue(ViewInquiryDetailsActivity.this);
        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(
                Request.Method.GET,
                URL,
                null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {

                        try {

                            for (int index = 0; index < response.length(); index++) {

                                JSONArray responseData = response.getJSONArray(index);

                                String idNumber = ((Number) responseData.get(0)).toString();
                                String imageName = (String) responseData.get(3);
                                String imageUrl =  API.INQUIRY_ASSERT_URL + id + "/images/" +  imageName;

                                imagesArrayList.add(new Images(idNumber, imageUrl));

                            }

                            imagesAdapter.notifyDataSetChanged();

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(ViewInquiryDetailsActivity.this, error.toString(),Toast.LENGTH_SHORT).show();
                    }
                }

        );

        requestQueue.add(jsonArrayRequest);

    }

    private void showVideo()
    {
        String URL = API.INQUIRIES_API + "/" + id + "/video";

        RequestQueue requestQueue = Volley.newRequestQueue(ViewInquiryDetailsActivity.this);
        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(
                Request.Method.GET,
                URL,
                null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {

                        try {

                            int count = response.length();
                            if (count == 1) {
                                btnViewVideo.setVisibility(View.VISIBLE);

                                JSONArray responseData = response.getJSONArray(0);

                                String videoUrl = (String) responseData.get(3);
                                inquiryVideoUrl = videoUrl;
                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(ViewInquiryDetailsActivity.this, error.toString(),Toast.LENGTH_SHORT).show();
                    }
                }

        );

        requestQueue.add(jsonArrayRequest);

    }

}

class Images {

    String id, image;

    public Images(String id, String image) {
        this.id = id;
        this.image = image;
    }

    public String getId() {
        return id;
    }

    public String getImage() {
        return image;
    }
}

class ImagesAdapter extends RecyclerView.Adapter<ImagesAdapter.ImagesHolder> {

    private List<Images> imagesList;
    class ImagesHolder extends RecyclerView.ViewHolder {
        TextView name;
        ImagesHolder(View view) {
            super(view);
            name = view.findViewById(R.id.name);
        }
    }
    public ImagesAdapter(List<Images> imagesList) {
        this.imagesList = imagesList;
    }
    @NonNull
    @Override
    public ImagesHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.row_image_item, parent, false);
        return new ImagesHolder(itemView);
    }
    @Override
    public void onBindViewHolder(ImagesHolder holder, int position) {
        Images images = imagesList.get(position);
        holder.name.setText("Image " + images.getId());
    }
    @Override
    public int getItemCount() {
        return imagesList.size();
    }

}