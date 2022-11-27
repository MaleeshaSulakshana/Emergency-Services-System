package com.example.ess.Classes;

public class API {

    //    Base api
    public static final String BASE_URL = "http://192.168.1.4:5000";

    //    User api
    public static final String USER_API = BASE_URL + "/users";
    //    Department api
    public static final String DEPARTMENT_API = BASE_URL + "/departments";
    //    Branches api
    public static final String BRANCHES_API = BASE_URL + "/branches";
    //    Inquiries api
    public static final String INQUIRIES_API = BASE_URL + "/inquiries";

    //    Assert api
    public static final String ASSERT_URL = BASE_URL + "/static/images";

    public static final String DEPARTMENTS_ASSERT_URL = ASSERT_URL + "/departments_images";

    public static final String PROFILE_ASSERT_URL = ASSERT_URL + "/users_profile_pic";

    public static final String INQUIRY_ASSERT_URL = ASSERT_URL + "/inquiries";


}
